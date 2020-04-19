import React from 'react';
import { Container } from '@material-ui/core';
import styled from 'styled-components';
import {BottomBar, TopBar} from "../components";
import Loader from "../assets/koscielnik.gif";
import ReactMarkdown from "react-markdown";

const MemesContainer = styled(Container)`
`;

function Memes() {
  const input = '# This is a header\n\nAnd this is a paragraph';
  return (
    <>
      <TopBar title="Feature in progress"/>
      <MemesContainer>
        {/*<img src={Loader} alt=""/>*/}
        <ReactMarkdown source={input}/>
      </MemesContainer>
      <BottomBar/>
    </>
  )
}

export default Memes;
