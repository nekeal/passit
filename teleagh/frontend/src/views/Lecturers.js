import React from 'react';
import { Container } from '@material-ui/core';
import styled from 'styled-components';
import {BottomBar, TopBar} from "../components";
import Loader from "../assets/koscielnik.gif";

const LecturersContainer = styled(Container)`
`;

function Lecturers() {
  return (
    <>
      <TopBar title="Feature in progress"/>
      <LecturersContainer>
        <img src={Loader} alt=""/>
      </LecturersContainer>
      <BottomBar/>
    </>
  )
}

export default Lecturers;
