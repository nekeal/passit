import React from 'react';
import { useHistory } from "react-router";
import { useForm, Controller } from 'react-hook-form';
import { Container, Button, TextField, Typography } from '@material-ui/core';
import styled from 'styled-components';
import { authService } from '../../services';
import logo from '../../assets/logo.png';

const LoginContainer = styled(Container)`
  display: flex;
  flex-direction: column; 
  align-items: center;
  
  .logo {
    width: 10rem;
  }
  
  .header {
    font-size: 1.3rem;
    font-weight: 500;
    text-transform: uppercase;
    margin-bottom: 3rem;
  }
  
  .subheader {
    margin-bottom: 1rem;
  }
  
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

function Login() {
  const { handleSubmit, errors, setError, control } = useForm();
  const history = useHistory();

  const onSubmit = data => {
    const { username, password } = data;
    authService.login(username, password)
      .then(() => {
        history.push('/');
      })
      .catch((error) => {
        if(error.username) { setError('username', 'serverError', error.username.join(" ")); }
        if(error.password) { setError('password', 'serverError', error.password.join(" ")); }
        if(error.detail) { setError('password', 'serverError', error.detail); }
      });
  };

  return (
    <LoginContainer>
      <img className="logo" src={logo} alt="PassIt logo"/>
      <Typography className="header" component="h1">Pass your experience</Typography>
      <Typography className="subheader" component="h5">Cześć! Zaloguj się, aby kontynuować.</Typography>
      <form className="form" onSubmit={handleSubmit(onSubmit)}>
        <Controller name="username" defaultValue="" control={control} rules={{ required: "Pole jest wymagane" }} as={
          <TextField className="form-field" name="username" label="adres e-mail lub nazwa użytkownika" error={!!errors.username} helperText={errors.username && errors.username.message} />
        } />
        <Controller name="password" defaultValue="" control={control} rules={{ required: "Pole jest wymagane" }} as={
          <TextField className="form-field" name="password" label="hasło" error={!!errors.password} helperText={errors.password && errors.password.message}/>
        } />
        <Button className="submit-button" type="submit" variant="contained" color="primary">Zaloguj</Button>
      </form>
    </LoginContainer>
  )
}

export default Login;
