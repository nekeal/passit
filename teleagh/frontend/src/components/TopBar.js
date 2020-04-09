import React, {useState} from 'react';
import { AppBar, Toolbar, Typography, Backdrop, IconButton } from "@material-ui/core";
import Icon from "./Icon";
import Settings from "./Settings";
import {useHistory} from "react-router";
import { APP_ROUTES } from "../consts/routes";

function TopBar({ title, onFagChange, allowBack, desktopView }) {
  const [settingsOpen, setSettingsOpen] = useState(false);
  const history = useHistory();

  return (
    <AppBar position="sticky" color='default'>
      <Toolbar style={{ justifyContent: "space-between" }}>
        <div style={{ display: "flex" }}>
          { allowBack &&
            <div onClick={() => history.goBack()} style={{ marginRight: "1rem" }}>
              <Icon name='back' size='big'/>
            </div>
          }
          <Typography variant="h5">{ title }</Typography>
        </div>
        <div>
          {
            desktopView && (
              <>
                <IconButton href={APP_ROUTES.DASHBOARD}><Icon name="home" size="big"/></IconButton>
                <IconButton href={APP_ROUTES.SUBJECTS}><Icon name="resources" size="big"/></IconButton>
                <IconButton href={APP_ROUTES.LECTURERS}><Icon name="lecturer" size="big"/></IconButton>
                <IconButton href={APP_ROUTES.MEMES}><Icon name="meme" size="big"/></IconButton>
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
    </AppBar>
  );
}

export default TopBar;
