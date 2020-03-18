import React, {useState, useRef} from 'react';
import { useHistory } from "react-router";
import { useForm, Controller } from 'react-hook-form';
import { Container, Button, TextField, Typography, InputAdornment, IconButton, Snackbar } from '@material-ui/core';
// import { Alert } from '@material-ui/lab';
import styled from 'styled-components';
import { authService } from '../services';
import logo from '../assets/logo.png';
import Icon from '../components/Icon';
import {BottomBar, TopBar} from "../components";

const PasswordChangeContainer = styled(Container)`
  display: flex;
  flex-direction: column; 
  align-items: center;
  margin-top: 2rem;

  .form {
    width: 90%;
    display: flex;
    flex-direction: column;
    align-items: center;
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

function PasswordChange() {
  const [ showCurrentPass, setShowCurrentPass ] = useState(false);
  const [ showNewPass, setShowNewPass ] = useState(false);
  const [ showRepeatNewPass, setShowRepeatNewPass ] = useState(false);

  const { handleSubmit, errors, setError, control, watch } = useForm();
  const history = useHistory();
  const password = useRef({});
  password.current = watch("newPassword", "");

  const onSubmit = data => {
    const { currentPassword, newPassword } = data;
    authService.changePassword(currentPassword, newPassword)
      .then(() => {
        history.push('/');
      })
      .catch((error) => {
        if(error.currentPassword) { setError('currentPassword', 'serverError', error.currentPassword.join(" ")); }
        if(error.newPassword) { setError('newPassword', 'serverError', error.newPassword.join(" ")); }
      });
  };

  return (
    <>
      <TopBar title="Zmiana hasła"/>
      <PasswordChangeContainer>
        <form className="form" onSubmit={handleSubmit(onSubmit)}>
          <Controller name="currentPassword" defaultValue="" control={control} rules={{ required: "Pole jest wymagane" }} as={
            <TextField
              className="form-field"
              type={showCurrentPass ? "text" : "password"}
              name="currentPassword"
              label="Bieżące hasło"
              error={!!errors.currentPassword}
              helperText={errors.currentPassword && errors.currentPassword.message}
              InputProps={{
                endAdornment: <InputAdornment position="end">
                  <IconButton
                    aria-label="toggle password visibility"
                    onClick={() => setShowCurrentPass(!showCurrentPass)}
                    edge="end"
                  >
                    <Icon name={showCurrentPass ? 'eyeOpen' : 'eyeClosed'} />
                  </IconButton>
                </InputAdornment>
              }}
            />
          } />
          <Controller name="newPassword" defaultValue="" control={control} rules={{ required: "Pole jest wymagane" }} as={
            <TextField
              className="form-field"
              type={showNewPass ? "text" : "password"}
              name="newPassword"
              label="Nowe hasło"
              error={!!errors.newPassword}
              helperText={errors.newPassword && errors.newPassword.message}
              InputProps={{
                endAdornment: <InputAdornment position="end">
                  <IconButton
                    aria-label="toggle password visibility"
                    onClick={() => setShowNewPass(!showNewPass)}
                    edge="end"
                  >
                    <Icon name={showNewPass ? 'eyeOpen' : 'eyeClosed'} />
                  </IconButton>
                </InputAdornment>
              }}
            />
          } />
          <Controller name="newPasswordRepeat" defaultValue="" control={control} rules={{ required: "Pole jest wymagane", validate: value => value === password.current || "Hasła się nie zgadzają" }} as={
            <TextField
              className="form-field"
              type={showRepeatNewPass ? "text" : "password"}
              name="newPasswordRepeat"
              label="Powtórz nowe hasło"
              error={!!errors.newPasswordRepeat}
              helperText={errors.newPasswordRepeat && errors.newPasswordRepeat.message}
              InputProps={{
                endAdornment: <InputAdornment position="end">
                  <IconButton
                    aria-label="toggle password visibility"
                    onClick={() => setShowRepeatNewPass(!showRepeatNewPass)}
                    edge="end"
                  >
                    <Icon name={showRepeatNewPass ? 'eyeOpen' : 'eyeClosed'} />
                  </IconButton>
                </InputAdornment>
              }}
            />
          } />
          <IconButton>
            <Icon name="accept"/>
          </IconButton>
          {/*<Snackbar open={true} autoHideDuration={6000}>*/}
          {/*  <Alert severity="success">*/}
          {/*    This is a success message!*/}
          {/*  </Alert>*/}
          {/*</Snackbar>*/}

          {/*<Button className="submit-button" type="submit" variant="outlined" color="secondary">Zaloguj</Button>*/}
        </form>
      </PasswordChangeContainer>
      <BottomBar/>
    </>
  )
}

export default PasswordChange;
