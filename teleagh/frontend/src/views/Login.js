import React, {useState} from 'react';
import { useHistory } from "react-router";
import { useForm, Controller } from 'react-hook-form';
import { Container, Button, TextField, Typography, InputAdornment, IconButton } from '@material-ui/core';
import styled from 'styled-components';
import { authService } from '../services';
import logo from '../assets/logo.png';
import Icon from '../components/Icon';

//background-color: ${props => props.theme.bgColor};

const LoginContainer = styled(Container)`
  display: flex;
  flex-direction: column; 
  align-items: center;
  min-height: 100vh;
  
  .logo {
    width: 10rem;
    margin: 2rem 0;
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
  const [ showPassword, setShowPassword ] = useState(false);
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
      <Typography className="subheader" component="h5">Cześć! Zaloguj się, aby kontynuować.</Typography>
      <form className="form" onSubmit={handleSubmit(onSubmit)}>
        <Controller name="username" defaultValue="" control={control} rules={{ required: "Pole jest wymagane" }} as={
          <TextField
            className="form-field"
            type="text"
            name="username"
            label="adres e-mail lub nazwa użytkownika"
            error={!!errors.username}
            helperText={errors.username && errors.username.message}
          />
        } />
        <Controller name="password" defaultValue="" control={control} rules={{ required: "Pole jest wymagane" }} as={
          <TextField
            className="form-field"
            type={showPassword ? "text" : "password"}
            name="password"
            label="hasło"
            error={!!errors.password}
            helperText={errors.password && errors.password.message}
            InputProps={{
              endAdornment: <InputAdornment position="end">
                <IconButton
                  aria-label="toggle password visibility"
                  onClick={() => setShowPassword(!showPassword)}
                  edge="end"
                >
                  <Icon name={showPassword ? 'eyeOpen' : 'eyeClosed'} />
                </IconButton>
              </InputAdornment>
            }}
          />
        } />
        <Button className="submit-button" type="submit" variant="outlined" color="secondary">Zaloguj</Button>
      </form>
    </LoginContainer>
  )
}

export default Login;
