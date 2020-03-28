import React, {useEffect, useState} from 'react';
import {Typography, Paper, IconButton, TextField, Button, Link} from "@material-ui/core";
import Icon from "./Icon";
import styled from "styled-components";
import { Controller, useForm } from "react-hook-form";
import {newsService} from "../services";
import Autocomplete from '@material-ui/lab/Autocomplete';

const NewsEditContainer = styled(Paper)`
  width: 90%;
  border-radius: 1rem;
  padding: 0.5rem;
  
  .form {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin-bottom: 3rem;
  }
  
  .header {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .form-field {
    width: 90%;
    margin-bottom: 0.5rem;
  }
  
  .attachment {
    margin-top: 1.25rem;
    display: flex;
    align-items: center;
    font-style: italic;
    width: 90%;
    justify-content: center;
    margin-bottom: 1.25rem;
    
    .filename {
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      padding-right: 0.3rem;
    }
    
    img {
      margin-left: 0.75rem;
    }
  }

  
`;

function NewsEdit({ news, sags, onAccept, onDecline }) {
  const { register, handleSubmit, errors, setValue, setError, getValues, control } = useForm();
  const [ sagSelected, setSagSelected ] = useState(null);
  const [ loading, setLoading ] = useState(false);
  const [ filename, setFilename ] = useState(undefined);

  const onSubmit = data => {
    setLoading(true);
    onAccept(data).catch(error => {
      if(error.title) { setError('title', 'serverError', error.title.join(" ")); }
      if(error.content) { setError('content', 'serverError', error.content.join(" ")); }
      if(error.sag) { setError('sag', 'serverError', error.sag.join(" ")); }
      setLoading(false);
    });
  };

  useEffect(() => {
    if(news) {
      const { title, content, sag, attachment } = news;
      setValue("title", title);
      setValue("content", content);
      setValue("sag", sag);
      setFilename(attachment.filename);
      setSagSelected(sags.find(s => s.id === sag));
    }
  }, [news, setValue]);

  useEffect(() => {
    register({ name: "sag" });
    register({ name: "attachment" });
  }, [register]);

  const attachmentAdd = (e) => {
    e.persist();
    setFilename(e.target.files[0].name);
    setValue("attachment", e.target.files[0]);
  };

  const attachmentRemove = () => {
    setFilename(undefined);
    setValue("attachment", undefined);
  };

  return (
    <NewsEditContainer onClick={e => e.stopPropagation()}>
      <form className="form" onSubmit={handleSubmit(onSubmit)}>
        <div className="header">
          <IconButton onClick={onDecline}><Icon name="decline"/></IconButton>
          <Typography variant="h6" >{ news ? "Edytuj ogłoszenie" : "Dodaj ogłoszenie" }</Typography>
          {
            loading ?
              <IconButton disabled><Icon name="loader"/></IconButton> :
              <IconButton type="submit"><Icon name="accept"/></IconButton>
          }
        </div>
        {
          filename ?
            <div className="attachment">
              <div className="filename">{ filename }</div>
              <Icon name="decline" size="small" onClick={attachmentRemove}/>
            </div>
            :
            <Button component="label" startIcon={<Icon name="attachment" size="big"/>}>
              Dodaj załącznik
              <input
                type="file"
                style={{ display: "none" }}
                onChange={attachmentAdd}
              />
            </Button>
        }
        <Controller name="title" defaultValue="" control={control} rules={{ required: "Pole jest wymagane" }} as={
          <TextField
            className="form-field"
            type="text"
            name="title"
            label="Tytuł ogłoszenia"
            error={!!errors.title}
            helperText={errors.title && errors.title.message}
          />
        } />
        <Controller name="content" defaultValue="" control={control} rules={{ required: "Pole jest wymagane" }} as={
          <TextField
            className="form-field"
            type="text"
            name="content"
            label="Treść ogłoszenia"
            multiline
            error={!!errors.content}
            helperText={errors.content && errors.content.message}
          />
        } />
        <Autocomplete
          className="form-field"
          value={sagSelected}
          onChange={(e, option) => {
            if(option) {
              setSagSelected(option);
              setValue("sag", option.id);
            } else {
              setSagSelected(null);
              setValue("sag", undefined);
            }
          }}
          options={sags}
          getOptionLabel={option => option.subjectName || ""}
          renderInput={params =>
            <TextField
              {...params}
              name="sag"
              label="Przedmiot"
            />
          }
        />
      </form>
    </NewsEditContainer>
  );
}

export default NewsEdit;
