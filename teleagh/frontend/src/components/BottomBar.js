import React from 'react';
import {BottomNavigation, BottomNavigationAction} from "@material-ui/core";
import Icon from "./Icon";
import styled from "styled-components";
import {useHistory, useLocation} from "react-router";
import { APP_ROUTES } from "../consts/routes";
import { useTranslation } from 'react-i18next';

const BottomNavigationContainer = styled(BottomNavigation)`
  position: fixed;
  width: 100%;
  bottom: 0;
  box-shadow: 0px 4px 5px rgba(0, 0, 0, 0.2), 0px 3px 14px rgba(0, 0, 0, 0.12), 0px 8px 10px rgba(0, 0, 0, 0.14);
`;

function BottomBar() {
  const location = useLocation();
  const history = useHistory();
  const { t } = useTranslation();

  return (
    <BottomNavigationContainer value={location.pathname} onChange={(event, newValue) => history.push(newValue)} showLabels>
      <BottomNavigationAction label={t("HOME")} value={APP_ROUTES.DASHBOARD} icon={<Icon name='home'/>} />
      <BottomNavigationAction label={t("SUBJECTS")} value={APP_ROUTES.SUBJECTS} icon={<Icon name='resources'/>} />
      <BottomNavigationAction label={t("LECTURERS")} value={APP_ROUTES.LECTURERS} icon={<Icon name='lecturer'/>} />
      <BottomNavigationAction label={t("MEMES")} value={APP_ROUTES.MEMES} icon={<Icon name='meme'/>} />
    </BottomNavigationContainer>

  );
}

export default BottomBar;
