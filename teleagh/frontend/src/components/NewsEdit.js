import React, {useEffect, useState} from 'react';
import { Typography, Paper, IconButton, TextField } from "@material-ui/core";
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
    margin-bottom: 1rem;
  }
  
  .form-field {
    width: 90%;
    margin-bottom: 0.5rem;
  }
  
  
`;

function NewsEdit({ news, sags, onAdd, onClose }) {
  const { register, handleSubmit, errors, setValue, setError, getValues, control } = useForm();
  const [ sagSelected, setSagSelected ] = useState(null);

  const onSubmit = data => {
    onAdd(data);
  };

  useEffect(() => {
    if(news) {
      const { title, content, sag } = news;
      setValue("title", title);
      setValue("content", content);
      setValue("sag", sag);
    }
  }, [news, setValue]);

  useEffect(() => {
    register({ name: "sag" })
  }, [register]);

  return (
    <NewsEditContainer onClick={e => e.stopPropagation()}>
      <form className="form" onSubmit={handleSubmit(onSubmit)}>
        <div className="header">
          <IconButton onClick={onClose}><Icon name="decline"/></IconButton>
          <Typography variant="h6" >{ news ? "Edytuj ogłoszenie" : "Dodaj ogłoszenie" }</Typography>
          <IconButton type="submit"><Icon name="accept"/></IconButton>
        </div>
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
