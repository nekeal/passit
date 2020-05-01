import React, {useEffect, useReducer, useState} from 'react';
import {Typography, Paper, IconButton, TextField, Button, InputAdornment} from "@material-ui/core";
import Icon from "./Icon";
import styled from "styled-components";
import { Controller, useForm } from "react-hook-form";
import {useTranslation} from "react-i18next";
import { EditDialog } from "../consts/styles";

const OpinionEditContainer = styled(EditDialog)`  
`;


function EventEdit({ event, onAccept, onDecline }) {
  const { register, handleSubmit, errors, setValue, setError, getValues, control } = useForm();
  const [ loading, setLoading ] = useState(false);
  const { t } = useTranslation();

  const onSubmit = data => {
    onAccept(data).catch(error => {
      if(error.content) { setError('content', 'serverError', error.content.join(" ")); }
    });
  };

  useEffect(() => {
    if(opinion) {
      const { content } = opinion;
      setValue("content", content);
    }
  }, [opinion, setValue]);


  return (
    <OpinionEditContainer onClick={e => e.stopPropagation()}>
      <form className="form" onSubmit={handleSubmit(onSubmit)}>
        <div className="header">
          <IconButton onClick={onDecline} className="form-action"><Icon name="decline" clickable/></IconButton>
          <Typography variant="h6" >{ opinion ? t("EDIT_OPINION") : t("ADD_OPINION") }</Typography>
          {
            loading ?
              <IconButton disabled><Icon name="loader"/></IconButton> :
              <IconButton type="submit" className="form-action accept"><Icon name="accept" clickable/></IconButton>
          }
        </div>
        <Controller name="content" defaultValue="" control={control} rules={{ required: t("REQUIRED_FIELD") }} as={
          <TextField
            className="form-field"
            type="text"
            name="content"
            label={t("OPINION_CONTENT")}
            multiline
            error={!!errors.content}
            helperText={errors.content && errors.content.message}
          />
        } />
      </form>
    </OpinionEditContainer>
  );
}

export default EventEdit;
