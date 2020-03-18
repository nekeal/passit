import React from 'react';
import { Container } from '@material-ui/core';
import styled from 'styled-components';
import {BottomBar, TopBar} from "../components";

const LecturersContainer = styled(Container)`
`;

function Lecturers() {
  return (
    <>
      <TopBar title="Prowadzący"/>
      <LecturersContainer>
        Prowadzący
      </LecturersContainer>
      <BottomBar/>
    </>
  )
}

export default Lecturers;
