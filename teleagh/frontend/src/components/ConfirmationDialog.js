import React from 'react';
import { Dialog, DialogTitle, DialogContent, DialogContentText, DialogActions, Button, IconButton } from "@material-ui/core";
import styled from 'styled-components';
import Icon from "./Icon";
import {useTranslation} from "react-i18next";

const DialogContainer = styled(Dialog)`
  .MuiDialog-paper {
    border-radius: 1rem;
    margin: 1rem;
  }
  
  .MuiDialogTitle-root {
    padding: 1.25rem;
  }
    
  .MuiDialogActions-root {
    padding: 0 1.25rem 1.25rem;
    display: flex;
    justify-content: space-between;
  }
`;

function ConfirmationDialog({ open, onAccept, onDecline }) {
  const { t } = useTranslation();

  return (
    <DialogContainer open={open}>
      <DialogTitle id="alert-dialog-title">{t("CONFIRM_ANNOUNCEMENT_DELETION")}</DialogTitle>
      <DialogActions>
        <IconButton onClick={onDecline}>
          <Icon name="decline" clickable/>
        </IconButton>
        <IconButton onClick={onAccept}>
          <Icon name="accept" clickable/>
        </IconButton>
      </DialogActions>
    </DialogContainer>
  )
}

export default ConfirmationDialog;
