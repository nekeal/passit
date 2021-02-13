import React from 'react';
import {Container, useMediaQuery} from '@material-ui/core';
import styled from 'styled-components';
import {BottomBar, TopBar} from "../components";
import Loader from "../assets/koscielnik.gif";

const MemesContainer = styled(Container)`
`;

function Memes() {
  const desktopView = useMediaQuery("(min-width:800px)");

  return (
    <>
      <TopBar desktopView={desktopView} title="Feature in progress"/>
      <MemesContainer>
        {/*<img src={Loader} alt=""/>*/}
      </MemesContainer>
      {
        !desktopView && <BottomBar/>
      }
    </>
  )
}

export default Memes;
