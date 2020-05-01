import React from 'react';
import { useHistory } from "react-router";
import { Container, Typography } from '@material-ui/core';
import styled from 'styled-components';
import logo from '../assets/logo.png';
import {useTranslation} from "react-i18next";

const ConnectionProblemContainer = styled(Container)`
  &.MuiContainer-root {
    display: flex;
    flex-direction: column; 
    align-items: center;
    min-height: 100vh;
    cursor: pointer;
  }
  
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
  const { t } = useTranslation();

  return (
    <ConnectionProblemContainer onClick={() => history.goBack()}>
      <img className="logo" src={logo} alt="PassIt logo"/>
      <Typography className="subheader" component="h5">{t("COONECTION_PROBLEM")}<br/>{t("TAP_TO_TRY_AGAIN")}</Typography>
    </ConnectionProblemContainer>
  )
}

export default ConnectionProblem;
