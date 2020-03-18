import React from 'react';
import { useHistory } from "react-router";
import { Container, Typography } from '@material-ui/core';
import styled from 'styled-components';
import logo from '../assets/logo.png';

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

function ConnectionProblem() {
  const history = useHistory();

  return (
    <LoginContainer>
      <img className="logo" src={logo} alt="PassIt logo"/>
      <Typography className="subheader" component="h5">Ups, wystąpił problem z łącznością :( Stuknij w ekran, aby spróbować ponownie.</Typography>
    </LoginContainer>
  )
}

export default ConnectionProblem;
