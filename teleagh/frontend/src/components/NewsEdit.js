import React, {useEffect, useState} from 'react';
import {Typography, Paper, IconButton, TextField, Button, Link, InputAdornment} from "@material-ui/core";
import Icon from "./Icon";
import styled from "styled-components";
import { Controller, useForm } from "react-hook-form";
import {newsService} from "../services";
import Autocomplete from '@material-ui/lab/Autocomplete';
import {useTranslation} from "react-i18next";
import ReactMarkdown from "react-markdown";

const NewsEditContainer = styled(Paper)`
  width: 90%;
  border-radius: 1rem;
  padding: 0.5rem;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  
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
    margin-top: 0.7rem;
  }
  
  .add-attachment {
    margin-left: 1rem;
    align-self: flex-start; 
  }
  
  .content-input {
    display: ${props => props.preview ? "none" : "inline-flex"};
  }
  
  .content-preview {
    width: 90%;
    position: relative;
    display: ${props => props.preview ? "block" : "none"};
    
    .preview-close {
      position: absolute;
      top: 50%;
      right: 0;
      transform: translateY(-50%);
    }
  }
  
  .attachment {
    margin: 1rem 1.5rem;
    align-self: flex-start; 
    display: flex;
    align-items: center;
    font-style: italic;
    justify-content: flex-start;
    
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
  const [ showPreview, setShowPreview ] = useState(false);
  const { t } = useTranslation();

  const onSubmit = data => {
    setLoading(true);
    onAccept(data).catch(error => {
      if(error.title) { setError('title', 'serverError', error.title.join(" ")); }
      if(error.content) { setError('content', 'serverError', error.content.join(" ")); }
      if(error.sag) { setError('sag', 'serverError', error.sag.join(" ")); }
      setLoading(false);
    });
  };

  const content = getValues().content;

  useEffect(() => {
    if(news) {
      const { title, content, sag, attachment } = news;
      setValue("title", title);
      setValue("content", content);
      setValue("sag", sag);
      setSagSelected(sags.find(s => s.id === sag));
      attachment && setFilename(attachment.filename);
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
    <NewsEditContainer onClick={e => e.stopPropagation()} preview={showPreview ? 1 : 0}>
      <form className="form" onSubmit={handleSubmit(onSubmit)}>
        <div className="header">
          <IconButton onClick={onDecline}><Icon name="decline"/></IconButton>
          <Typography variant="h6" >{ news ? t("EDIT_ANNOUNCEMENT") : t("ADD_ANNOUNCEMENT") }</Typography>
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
            <Button className="add-attachment" component="label" startIcon={<Icon name="attachment" size="big"/>}>
              {t("ADD_ATTACHMENT")}
              <input
                type="file"
                style={{ display: "none" }}
                onChange={attachmentAdd}
              />
            </Button>
        }
        <Controller name="title" defaultValue="" control={control} rules={{ required: t("REQUIRED_FIELD") }} as={
          <TextField
            className="form-field"
            type="text"
            name="title"
            label={t("ANNOUNCEMENT_TITLE")}
            error={!!errors.title}
            helperText={errors.title && errors.title.message}
          />
        } />
        <div className="content-preview">
          <ReactMarkdown source={content}/>
          <IconButton
            className="preview-close"
            tabIndex="-1"
            onClick={() => setShowPreview(false)}
          >
            <Icon name="eyeOpen" clickable/>
          </IconButton>
        </div>
        <Controller name="content" defaultValue="" control={control} rules={{ required: t("REQUIRED_FIELD") }} as={
          <TextField
            className="form-field content-input"
            type="text"
            name="content"
            label={t("ANNOUNCEMENT_CONTENT")}
            multiline
            error={!!errors.content}
            helperText={errors.content && errors.content.message}
            InputProps={{
              endAdornment: <InputAdornment position="end">
                <IconButton
                  tabIndex="-1"
                  edge="end"
                  onClick={() => setShowPreview(true)}
                >
                  <Icon name="eyeClosed" clickable />
                </IconButton>
              </InputAdornment>
            }}
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
              label={t("SUBJECT")}
            />
          }
        />
      </form>
    </NewsEditContainer>
  );
}

export default NewsEdit;
