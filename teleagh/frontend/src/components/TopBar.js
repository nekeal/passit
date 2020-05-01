import React, {useState} from 'react';
import { AppBar, Toolbar, Typography, Backdrop, IconButton } from "@material-ui/core";
import Icon from "./Icon";
import Settings from "./Settings";
import {useHistory, useLocation} from "react-router";
import { Link } from "react-router-dom";
import { APP_ROUTES } from "../consts/routes";
import styled from "styled-components";
import logo from "../assets/logo.png";
import {useTranslation} from "react-i18next";

const TopBarContainer = styled(AppBar)`
  align-items: center;
  
  &.desktop.MuiPaper-root {
    background-color: transparent;
    box-shadow: none;
  }
  
  .logo {
    width: 5rem;
  }
  
  .MuiToolbar-root {
    justify-content: space-between;
    align-items: center;
    width: 100%;
    max-width: 1280px;
  }
  
  .title {
    display: flex;
  }
  
  .arrow-back {
    margin-right: 1rem;
  }
  
  .nav-items {
    position: relative;
    bottom: 0.3rem;
  }
  
  .nav-item {
    margin-left: 1rem;
  }
  
  .nav-name {
    font-size: 0.9rem;
    color: ${props => props.theme.mainViolet};
    position: absolute;
    bottom: -0.5rem;  }
`;

function TopBar({ title, onFagChange, allowBack, desktopView }) {
  const [settingsOpen, setSettingsOpen] = useState(false);
  const history = useHistory();
  const location = useLocation();
  const { t } = useTranslation();

  return (
    <TopBarContainer position="sticky" color="default" className={desktopView && "desktop"}>
      <Toolbar>
        <div className="title">
          {
            desktopView ?
              <Link to={APP_ROUTES.DASHBOARD}><img className="logo" src={logo} alt="PassIt logo"/></Link> :
              <>
                { allowBack &&
                <div onClick={() => history.goBack()} className="arrow-back">
                  <Icon name='back' size='big'/>
                </div>
                }
                <Typography variant="h5">{ title }</Typography>
              </>
          }
        </div>
        <div className="nav-items">
          {
            desktopView && (
              <>
                <IconButton href={APP_ROUTES.DASHBOARD} className="nav-item">
                  <Icon name="home" size="big" clickable/>
                  { location.pathname === APP_ROUTES.DASHBOARD && <div className="nav-name">{t("HOME")}</div>}
                </IconButton>
                <IconButton href={APP_ROUTES.SUBJECTS} className="nav-item">
                  <Icon name="resources" size="big" clickable/>
                  { location.pathname === APP_ROUTES.SUBJECTS && <div className="nav-name">{t("SUBJECTS")}</div>}
                </IconButton>
                <IconButton href={APP_ROUTES.LECTURERS} className="nav-item">
                  <Icon name="lecturer" size="big" clickable/>
                  { location.pathname === APP_ROUTES.LECTURERS && <div className="nav-name">{t("LECTURERS")}</div>}
                </IconButton>
                <IconButton href={APP_ROUTES.MEMES} className="nav-item">
                  <Icon name="meme" size="big" clickable/>
                  { location.pathname === APP_ROUTES.MEMES && <div className="nav-name">{t("MEMES")}</div>}
                </IconButton>
              </>
            )
          }
          <IconButton href="#" onClick={() => setSettingsOpen(!settingsOpen)}>
            <Icon name="settings" size="big" clickable/>
          </IconButton>
        </div>
      </Toolbar>
      <Backdrop open={settingsOpen} onClick={() => setSettingsOpen(false)}>
        { settingsOpen && <Settings onFagChange={onFagChange}/> }
      </Backdrop>
    </TopBarContainer>
  );
}

export default TopBar;
