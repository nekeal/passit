import React from "react";
import {Paper, Typography} from "@material-ui/core";
import styled from "styled-components";
import { styleHelpers } from "../consts/styles";
import Icon from "./Icon";

const LecturerContainer = styled(Paper)`
  ${styleHelpers.gradientBorder};
  padding: 1rem;
  margin-bottom: 1rem;
  
  display: flex;
  align-items: center;
  
  width: min(90%, 500px);
  
  .data {
    display: flex;
    flex-direction: column;
    margin-left: 0.5rem;
    
    .subjects {
      margin-top: 0.2px;
      color: rgba(55,54,54,0.7);
      font-style: italic;
    }
  }
`;

function LecturerTile({ lecturer }) {
  const { fullName } = lecturer;
  return (
    <LecturerContainer variant="outlined">
      <Icon name="lecturer"/>
      <div className="data">
        <Typography variant="h6">
          { fullName }
        </Typography>
        <div className="subjects">
          PO, Ruby, Tekstowe
        </div>
      </div>
    </LecturerContainer>

  );
}

export default LecturerTile;
