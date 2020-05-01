import React, {useEffect, useReducer} from 'react';
import {Typography, Paper, IconButton, TextField, Button, InputAdornment} from "@material-ui/core";
import Icon from "./Icon";
import styled from "styled-components";
import { Controller, useForm } from "react-hook-form";
import Autocomplete from '@material-ui/lab/Autocomplete';
import {useTranslation} from "react-i18next";
import ReactMarkdown from "react-markdown";
import { EditDialog } from "../consts/styles";

const NewsEditContainer = styled(EditDialog)`
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

const initialState = {
  sagSelected: {},
  filename: undefined,
  loading: false,
  showPreview: false
};

function reducer(state, action) {
  const { type, payload } = action;
  switch (type) {
    case "SUBMIT_INIT":
      return { ...state, loading: true };
    case "SUBMIT_ERROR":
      return { ...state, loading: false };
    case "SET_EDITED_NEWS_DATA":
      const { sag, attachment } = payload;
      return { ...state, sagSelected: sag, filename: attachment && attachment.filename };
    case "SHOW_CONTENT_PREVIEW":
      return { ...state, showPreview: true };
    case "HIDE_CONTENT_PREVIEW":
      return { ...state, showPreview: false };
    case "SET_SAG":
      return { ...state, sagSelected: payload };
    case "SET_FILENAME":
      return { ...state, filename: payload };
    default:
      return { ...state };
  }
}

function NewsEdit({ news, sags, onAccept, onDecline }) {
  const { register, handleSubmit, errors, setValue, setError, getValues, control } = useForm();
  const [ state, dispatch ] = useReducer(reducer, initialState);
  const { t } = useTranslation();

  const { sagSelected, loading, filename, showPreview } = state;

  const onSubmit = data => {
    dispatch({ type: "SUBMIT_INIT" });
    onAccept(data).catch(error => {
      if(error.title) { setError('title', 'serverError', error.title.join(" ")); }
      if(error.content) { setError('content', 'serverError', error.content.join(" ")); }
      if(error.sag) { setError('sag', 'serverError', error.sag.join(" ")); }
      dispatch({ type: "SUBMIT_ERROR" });
    });
  };

  const { content } = getValues();

  useEffect(() => {
    if(news) {
      const { title, content, sag, attachment } = news;
      setValue("title", title);
      setValue("content", content);
      setValue("sag", sag);
      dispatch({ type: "SET_EDITED_NEWS_DATA", payload: { sag: sags.find(s => s.id === sag), attachment } });
    }
  }, [news, setValue]);

  useEffect(() => {
    register({ name: "sag" });
    register({ name: "attachment" });
  }, [register]);

  const attachmentAdd = event => {
    event.persist();
    const { target: { files: [ file ] } } = event;
    dispatch({ type: "SET_FILENAME", payload: file.name });
    setValue("attachment", file);
  };

  const attachmentRemove = () => {
    dispatch({ type: "SET_FILENAME", payload: undefined });
    setValue("attachment", undefined);
  };

  const renderAttachmentField = () =>
    filename
      ?
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
  ;

  const renderTitleField = () =>
    <Controller name="title" defaultValue="" control={control} rules={{ required: t("REQUIRED_FIELD") }} as={
      <TextField
        className="form-field"
        type="text"
        name="title"
        label={t("ANNOUNCEMENT_TITLE")}
        error={!!errors.title}
        helperText={errors.title && errors.title.message}
      />
    }/>;

  const renderPreview = () =>
    <div className="content-preview">
      <ReactMarkdown source={content}/>
      <IconButton
        className="preview-close"
        tabIndex="-1"
        onClick={() => dispatch({ type: "HIDE_CONTENT_PREVIEW" })}
      >
        <Icon name="eyeOpen" clickable/>
      </IconButton>
    </div>;

  const renderContentField = () =>
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
              onClick={() => dispatch({ type: "SHOW_CONTENT_PREVIEW" })}
            >
              <Icon name="eyeClosed" clickable />
            </IconButton>
          </InputAdornment>
        }}
      />
    } />;

  const renderSagField = () =>
    <Autocomplete
      className="form-field"
      value={sagSelected}
      onChange={(e, option) => {
        if(option) {
          dispatch({ type: "SET_SAG", payload: option });
          setValue("sag", option.id);
        } else {
          dispatch({ type: "SET_SAG", payload: undefined });
          setValue("sag", undefined);
        }
      }}
      options={sags}
      getOptionSelected={(option, value) => value && option.id === value.id}
      getOptionLabel={option => option.subjectName || ""}
      renderInput={params =>
        <TextField
          {...params}
          name="sag"
          label={t("SUBJECT")}
        />
      }
    />;


  return (
    <NewsEditContainer onClick={e => e.stopPropagation()} preview={showPreview ? 1 : 0}>
      <form className="form" onSubmit={handleSubmit(onSubmit)}>
        <div className="header">
          <IconButton onClick={onDecline} className="form-action"><Icon name="decline" clickable/></IconButton>
          <Typography variant="h6" >{ news ? t("EDIT_ANNOUNCEMENT") : t("ADD_ANNOUNCEMENT") }</Typography>
          {
            loading ?
              <IconButton disabled><Icon name="loader"/></IconButton> :
              <IconButton type="submit" className="form-action accept"><Icon name="accept" clickable/></IconButton>
          }
        </div>
        { renderAttachmentField() }
        { renderTitleField() }
        { showPreview && renderPreview() }
        { renderContentField() }
        { renderSagField() }
      </form>
    </NewsEditContainer>
  );
}

export default NewsEdit;
