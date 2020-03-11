import React, {useState} from 'react';
import {AppBar, Toolbar, Typography, Backdrop, Paper, ExpansionPanel, ExpansionPanelSummary, ExpansionPanelDetails, Switch, Button} from "@material-ui/core";
import Icon from "./Icon";
import styled from "styled-components";

const SettingsContainer = styled(Paper)`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  
  .profile {
    display: flex;
    align-items: center;
    padding: 1rem 0;
  }
  
  .profile-info {
    margin-left: 1rem;
  }
  
  .panel {
    width: 100%;
    margin: 0;
    box-shadow: none;
    border-top: 1px solid rgba(12, 11, 11, 0.25);
    &:last-child {
      border-bottom: 1px solid rgba(12, 11, 11, 0.25);
    }
  }
  
  .panel-details {
    display: flex;
    align-items: center;
  }
  
  .logout-button {
    margin: 3em 0 1em;
  }
`;

function TopBar() {
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [highContrast, setHighContrast] = useState(false);

  return (
    <AppBar position="sticky" color='default'>
      <Toolbar style={{ justifyContent: "space-between" }}>
        <Typography variant="h5">Główna</Typography>
        <div onClick={() => setSettingsOpen(!settingsOpen)}>
          <Icon name='settings' size='big'/>
        </div>
      </Toolbar>
      <Backdrop open={settingsOpen} onClick={() => setSettingsOpen(false)}>
        <SettingsContainer onClick={e => e.stopPropagation()}>
          <div className="profile">
            <div className="profile-icon">
              <Icon name="profile" size="huge" />
            </div>
            <div className="profile-info">
              <Typography variant="h5">Kamil Krzempek</Typography>
              <Typography>Zmień hasło</Typography>
            </div>
          </div>
          <div className="panel-container">
            <ExpansionPanel square className="panel">
              <ExpansionPanelSummary>
                <Typography variant="h6">Ułatwienia dostępu</Typography>
              </ExpansionPanelSummary>
              <ExpansionPanelDetails className="panel-details">
                <Typography>Zwiększ kontrast</Typography>
                <Switch
                  checked={highContrast}
                  onChange={() => setHighContrast(!highContrast)}
                  value="contrast"
                />
              </ExpansionPanelDetails>
            </ExpansionPanel>
            <ExpansionPanel square className="panel">
              <ExpansionPanelSummary>
                <Typography variant="h6">Wybór kierunku studiów</Typography>
              </ExpansionPanelSummary>
              <ExpansionPanelDetails className="panel-details">
                <Typography>Brak dostępnych kierunków studiów</Typography>
              </ExpansionPanelDetails>
            </ExpansionPanel>
          </div>
          <Button color="secondary" className="logout-button">Wyloguj się</Button>
        </SettingsContainer>
      </Backdrop>
    </AppBar>
  );
}

export default TopBar;
