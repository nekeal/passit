import React, {useState} from 'react';
import { AppBar, Toolbar, Typography, Backdrop } from "@material-ui/core";
import Icon from "./Icon";
import Settings from "./Settings";
import {useHistory} from "react-router";

function TopBar({ title, onFagChange, allowBack }) {
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
        <div onClick={() => setSettingsOpen(!settingsOpen)}>
          <Icon name='settings' size='big'/>
        </div>
      </Toolbar>
      <Backdrop open={settingsOpen} onClick={() => setSettingsOpen(false)}>
        { settingsOpen && <Settings onFagChange={onFagChange}/> }
      </Backdrop>
    </AppBar>
  );
}

export default TopBar;
