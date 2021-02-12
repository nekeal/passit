import React, {useEffect, useState} from 'react';
import { TextField} from "@material-ui/core";
import styled from "styled-components";
import { Controller, useForm } from "react-hook-form";
import {useTranslation} from "react-i18next";
import {EditDialog} from "../consts/styles";
import EditDialogHeader from "./EditDialogHeader";

const OpinionEditContainer = styled(EditDialog)`

`;


function OpinionEdit({ opinion, onAccept, onDecline }) {
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
        <EditDialogHeader
          text={opinion ? t("EDIT_OPINION") : t("ADD_OPINION")}
          loading={loading}
          onDecline={onDecline}
        />
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

export default OpinionEdit;
