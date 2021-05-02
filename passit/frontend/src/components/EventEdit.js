import React, {useEffect, useReducer, useState} from 'react';
import {Typography, Paper, IconButton, TextField, Button, InputAdornment} from "@material-ui/core";
import Icon from "./Icon";
import styled from "styled-components";
import { Controller, useForm } from "react-hook-form";
import {useTranslation} from "react-i18next";
import { EditDialog } from "../consts/styles";
import EditDialogHeader from "./EditDialogHeader";

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
    if(event) {
      const { content } = event;
      setValue("content", content);
    }
  }, [event, setValue]);


  return (
    <OpinionEditContainer onClick={e => e.stopPropagation()}>
      <form className="form" onSubmit={handleSubmit(onSubmit)}>
        <EditDialogHeader
          text={event ? t("EDIT_EVENT") : t("ADD_EVENT")}
          loading={loading}
          onDecline={onDecline}
        />
      </form>
    </OpinionEditContainer>
  );
}

export default EventEdit;
