import React, {useEffect, useState} from 'react';
import {
  Typography,
  Paper,
  ExpansionPanel,
  ExpansionPanelSummary,
  ExpansionPanelDetails,
  Switch,
  Button,
  Link
} from "@material-ui/core";
import Icon from "./Icon";
import styled from "styled-components";
import { authService, localStorageService } from "../services";
import {Link as RouterLink} from "react-router-dom";
import { useHistory } from "react-router-dom";
import {SubjectTile} from "./index";
import {APP_ROUTES} from "../consts/routes";

const SettingsContainer = styled(Paper)`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  width: 90%;
  
  .profile {
    display: flex;
    align-items: center;
    padding: 1rem 0;
  }
  
  .profile-info {
    margin-left: 1rem;
  }
  
  .panel-container {
    width: 90%;
  }
  
  .panel {
    width: 100%;
    margin: 0;
    box-shadow: none;
    border-top: 1px solid rgba(12, 11, 11, 0.25);
    &:last-child {
      border-bottom: 1px solid rgba(12, 11, 11, 0.25);
    }
    
    .MuiExpansionPanelSummary-content {
      display: flex;
      justify-content: center;
      margin: 1rem 0;
    }
  }
  
  .panel-details {
    display: flex;
    align-items: center;
    flex-direction: column;
  }
  
  .logout-button {
    margin: 3em 0 1em;
  }
  
  .fag-option {
    margin: 0.4rem 0;
    position: relative;
    
    &.selected {
      color: #87129A;
      &::before {
        content: '>';  
        position: absolute;
        left: -1rem;
      }
    }
  }
  
  .contrast-switch {
    display: flex;
    flex-direction: row;
    align-items: center;
  }
`;

function Settings({ onFagChange }) {
  const [highContrast, setHighContrast] = useState(false);
  const [profileInfo, setProfileInfo] = useState(undefined);
  const [activeFag, setActiveFag] = useState(1);
  const history = useHistory();

  useEffect(() => {
    authService.profileInfo().then(profileInfo => {
      setProfileInfo(profileInfo);
      setActiveFag(profileInfo.defaultFag.id);
    });
  }, []);

  return (
      <SettingsContainer onClick={e => e.stopPropagation()}>
        <div className="profile">
          <div className="profile-icon">
            <Icon name="profile" size="huge" />
          </div>
          <div className="profile-info">
            <Typography variant="h5">{profileInfo && profileInfo.fullName}</Typography>
            <Link component={RouterLink} to={`/password-change`}>Zmień hasło</Link>
          </div>
        </div>
        <div className="panel-container">
          <ExpansionPanel square className="panel">
            <ExpansionPanelSummary>
              <Typography variant="h6">Ułatwienia dostępu</Typography>
            </ExpansionPanelSummary>
            <ExpansionPanelDetails className="panel-details">
              <div className="contrast-switch">
                <Typography>Zwiększ kontrast</Typography>
                <Switch
                  checked={highContrast}
                  onChange={() => setHighContrast(!highContrast)}
                  value="contrast"
                />
              </div>
            </ExpansionPanelDetails>
          </ExpansionPanel>
          <ExpansionPanel square className="panel">
            <ExpansionPanelSummary>
              <Typography variant="h6">Wybór kierunku studiów</Typography>
            </ExpansionPanelSummary>
              {
                profileInfo &&
                <ExpansionPanelDetails className="panel-details">
                  { profileInfo.fags.map(fag =>
                    <Typography
                      className={fag.id === activeFag ? "fag-option selected" : "fag-option"}
                      onClick={() => {
                        authService.changeFAG(fag.id).then(() => {
                          setActiveFag(fag.id);
                          onFagChange && onFagChange();
                        });
                      }}
                      key={fag.id}
                    >{fag.name}</Typography>
                  ) }
                </ExpansionPanelDetails>
              }
          </ExpansionPanel>
        </div>
        <Button color="secondary" className="logout-button" onClick={() => {
          localStorageService.removeTokens();
          history.push(APP_ROUTES.LOGIN);
        }}>Wyloguj się</Button>
      </SettingsContainer>
  );
}

export default Settings;
