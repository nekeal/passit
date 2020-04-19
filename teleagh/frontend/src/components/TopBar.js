import React, {useState} from 'react';
import { AppBar, Toolbar, Typography, Backdrop, IconButton } from "@material-ui/core";
import Icon from "./Icon";
import Settings from "./Settings";
import {useHistory} from "react-router";
import { APP_ROUTES } from "../consts/routes";
import styled from "styled-components";
import logo from "../assets/logo.png";

const TopBarContainer = styled(AppBar)`
  align-items: center;
  
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
`;

function TopBar({ title, onFagChange, allowBack, desktopView }) {
  const [settingsOpen, setSettingsOpen] = useState(false);
  const history = useHistory();

  return (
    <TopBarContainer position="sticky" color="default">
      <Toolbar>
        <div className="title">
          {
            desktopView ?
              <img className="logo" src={logo} alt="PassIt logo"/> :
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
        <div>
          {
            desktopView && (
              <>
                <IconButton href={APP_ROUTES.DASHBOARD}><Icon name="home" size="big" clickable/></IconButton>
                <IconButton href={APP_ROUTES.SUBJECTS}><Icon name="resources" size="big" clickable/></IconButton>
                <IconButton href={APP_ROUTES.LECTURERS}><Icon name="lecturer" size="big" clickable/></IconButton>
                <IconButton href={APP_ROUTES.MEMES}><Icon name="meme" size="big" clickable/></IconButton>
              </>
            )
          }
          <IconButton href="#" onClick={() => setSettingsOpen(!settingsOpen)}>
            <Icon name='settings' size='big'/>
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
