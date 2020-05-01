import React from "react";
import {IconButton, Typography} from "@material-ui/core";
import Icon from "./Icon";
import styled from "styled-components";

const Container = styled.div`
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;

  .action {
    padding: 0.3rem 0.5rem 0.3rem 0.4rem;

    &.accept {
      border: 1px solid ${props => props.theme.mainViolet};
      border-radius: 0;
      box-shadow: 0px 4px 10px -3px rgba(0,0,0,0.4);
      clip-path: inset(0 0px -20px 0);
     }
  }
`;

function EditDialogHeader({ loading, onDecline, text }) {
  return (
    <Container>
      <IconButton onClick={onDecline} className="action"><Icon name="decline" clickable/></IconButton>
      <Typography variant="h6" >{ text }</Typography>
      {
        loading ?
          <IconButton disabled><Icon name="loader"/></IconButton> :
          <IconButton type="submit" className="action accept"><Icon name="accept" clickable/></IconButton>
      }
    </Container>
  )
}

export default EditDialogHeader;
