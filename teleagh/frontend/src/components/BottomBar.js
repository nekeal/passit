import React from 'react';
import {BottomNavigation, BottomNavigationAction} from "@material-ui/core";
import Icon from "./Icon";
import styled from "styled-components";
import {useHistory, useLocation} from "react-router";

const BottomNavigationContainer = styled(BottomNavigation)`
  position: fixed;
  width: 100%;
  bottom: 0;
  box-shadow: 0px 4px 5px rgba(0, 0, 0, 0.2), 0px 3px 14px rgba(0, 0, 0, 0.12), 0px 8px 10px rgba(0, 0, 0, 0.14);
`;

function BottomBar() {
  const location = useLocation();
  const history = useHistory();

  return (
    <BottomNavigationContainer value={location.pathname} onChange={(event, newValue) => history.push(newValue)} showLabels>
      <BottomNavigationAction label="Główna" value='/' icon={<Icon name='home'/>} />
      <BottomNavigationAction label="Przedmioty" value='/subjects' icon={<Icon name='resources'/>} />
      <BottomNavigationAction label="Prowadzący" value='/lecturers' icon={<Icon name='lecturer'/>} />
      <BottomNavigationAction label="Memy" value='/memes' icon={<Icon name='meme'/>} />
    </BottomNavigationContainer>

  );
}

export default BottomBar;
