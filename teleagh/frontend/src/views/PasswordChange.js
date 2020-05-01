import React, {useState, useRef} from 'react';
import { useHistory } from "react-router";
import { useForm, Controller } from 'react-hook-form';
import {
  Container,
  Button,
  TextField,
  InputAdornment,
  IconButton,
  useMediaQuery
} from '@material-ui/core';
import styled from 'styled-components';
import { authService } from '../services';
import Icon from '../components/Icon';
import {BottomBar, TopBar} from "../components";
import {SNACKBAR_TYPES} from "../consts/options";
import {useTranslation} from "react-i18next";

const PasswordChangeContainer = styled(Container)`
  &.MuiContainer-root {
    display: flex;
    flex-direction: column; 
    align-items: center;
    margin-top: 2rem;
  }

  .form {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: min(90%, 400px);
  }
  
  .form-field {
    width: 100%;
    margin-bottom: 1rem;
  }
  
  .submit-button {
    align-self: flex-end;
    margin-top: 2rem;
  }

`;

function PasswordChange({ setSnackbar }) {
  const [ showCurrentPass, setShowCurrentPass ] = useState(false);
  const [ showNewPass, setShowNewPass ] = useState(false);
  const [ showRepeatNewPass, setShowRepeatNewPass ] = useState(false);

  const desktopView = useMediaQuery("(min-width:800px)");

  const { handleSubmit, errors, setError, control, watch } = useForm();
  const history = useHistory();
  const password = useRef({});
  const { t } = useTranslation();

  password.current = watch("newPassword", "");

  const onSubmit = data => {
    const { currentPassword, newPassword } = data;
    authService.changePassword(currentPassword, newPassword)
      .then(() => {
        setSnackbar(SNACKBAR_TYPES.SUCCESS, "Hasło zmienione pomyślnie");
        history.push('/');
      })
      .catch((error) => {
        if(error.currentPassword) { setError('currentPassword', 'serverError', error.currentPassword.join(" ")); }
        if(error.newPassword) { setError('newPassword', 'serverError', error.newPassword.join(" ")); }
      });
  };

  return (
    <>
      <TopBar desktopView={desktopView} title={t("PASSWORD_CHANGE")}/>
      <PasswordChangeContainer>
        <form className="form" onSubmit={handleSubmit(onSubmit)}>
          <Controller name="currentPassword" defaultValue="" control={control} rules={{ required: t("REQUIRED_FIELD")}} as={
            <TextField
              className="form-field"
              type={showCurrentPass ? "text" : "password"}
              name="currentPassword"
              label={t("CURRENT_PASSWORD")}
              error={!!errors.currentPassword}
              helperText={errors.currentPassword && errors.currentPassword.message}
              InputProps={{
                endAdornment: <InputAdornment position="end">
                  <IconButton
                    tabIndex="-1"
                    onClick={() => setShowCurrentPass(!showCurrentPass)}
                    edge="end"
                  >
                    <Icon name={showCurrentPass ? 'eyeOpen' : 'eyeClosed'} clickable/>
                  </IconButton>
                </InputAdornment>
              }}
            />
          } />
          <Controller name="newPassword" defaultValue="" control={control} rules={{ required: t("REQUIRED_FIELD") }} as={
            <TextField
              className="form-field"
              type={showNewPass ? "text" : "password"}
              name="newPassword"
              label={t("NEW_PASSWORD")}
              error={!!errors.newPassword}
              helperText={errors.newPassword && errors.newPassword.message}
              InputProps={{
                endAdornment: <InputAdornment position="end">
                  <IconButton
                    tabIndex="-1"
                    onClick={() => setShowNewPass(!showNewPass)}
                    edge="end"
                  >
                    <Icon name={showNewPass ? 'eyeOpen' : 'eyeClosed'} clickable/>
                  </IconButton>
                </InputAdornment>
              }}
            />
          } />
          <Controller name="newPasswordRepeat" defaultValue="" control={control} rules={{ required: t("REQUIRED_FIELD"), validate: value => value === password.current || t("PASSWORDS_DONT_MATCH") }} as={
            <TextField
              className="form-field"
              type={showRepeatNewPass ? "text" : "password"}
              name="newPasswordRepeat"
              label={t("REPEAT_NEW_PASSWORD")}
              error={!!errors.newPasswordRepeat}
              helperText={errors.newPasswordRepeat && errors.newPasswordRepeat.message}
              InputProps={{
                endAdornment: <InputAdornment position="end">
                  <IconButton
                    tabIndex="-1"
                    aria-label="toggle password visibility"
                    onClick={() => setShowRepeatNewPass(!showRepeatNewPass)}
                    edge="end"
                  >
                    <Icon name={showRepeatNewPass ? 'eyeOpen' : 'eyeClosed'} clickable/>
                  </IconButton>
                </InputAdornment>
              }}
            />
          } />
          <Button className="submit-button" type="submit" variant="outlined" color="secondary">{t("PASSWORD_CHANGE")}</Button>
        </form>
      </PasswordChangeContainer>
      {
        !desktopView && <BottomBar/>
      }
    </>
  )
}

export default PasswordChange;
