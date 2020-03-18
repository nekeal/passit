import React from 'react';
import { Container } from '@material-ui/core';
import styled from 'styled-components';
import {BottomBar, TopBar} from "../components";
import Loader from "../assets/koscielnik.gif";

const MemesContainer = styled(Container)`
`;

function Memes() {
  return (
    <>
      <TopBar title={"Feature in progress"}/>
      <MemesContainer>
        <img src={Loader} alt=""/>
      </MemesContainer>
      <BottomBar/>
    </>
  )
}

export default Memes;
