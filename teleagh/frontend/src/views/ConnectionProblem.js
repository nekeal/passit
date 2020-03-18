import React from 'react';
import { useHistory } from "react-router";
import { Container, Typography } from '@material-ui/core';
import styled from 'styled-components';
import logo from '../assets/logo.png';

const ConnectionProblemContainer = styled(Container)`
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
    text-align: center;
  }
  
`;

function ConnectionProblem() {
  const history = useHistory();

  return (
    <ConnectionProblemContainer onClick={() => history.goBack()}>
      <img className="logo" src={logo} alt="PassIt logo"/>
      <Typography className="subheader" component="h5">Ups, wystąpił problem z łącznością :( <br/> Stuknij w ekran, aby spróbować ponownie.</Typography>
    </ConnectionProblemContainer>
  )
}

export default ConnectionProblem;
