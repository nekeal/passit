import React, {useState} from 'react';
import { AppBar, Toolbar, Typography, Backdrop } from "@material-ui/core";
import Icon from "./Icon";
import Settings from "./Settings";

function TopBar({ title }) {
  const [settingsOpen, setSettingsOpen] = useState(false);

  return (
    <AppBar position="sticky" color='default'>
      <Toolbar style={{ justifyContent: "space-between" }}>
        <Typography variant="h5">{ title }</Typography>
        <div onClick={() => setSettingsOpen(!settingsOpen)}>
          <Icon name='settings' size='big'/>
        </div>
      </Toolbar>
      <Backdrop open={settingsOpen} onClick={() => setSettingsOpen(false)}>
        { settingsOpen && <Settings/> }
      </Backdrop>
    </AppBar>
  );
}

export default TopBar;
