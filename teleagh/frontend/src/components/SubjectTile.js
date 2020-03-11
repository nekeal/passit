import React, {useState} from "react";
import {Paper, Typography, Link} from "@material-ui/core";
import Icon from "./Icon";
import styled from "styled-components";
import styleHelpers from "../helpers/styles";

const SubjectContainer = styled(Paper)`
  ${styleHelpers.gradientBorder};
  padding: 1rem;
  margin-bottom: 1rem;
  
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  .lecturer {
    margin-top: 0.5rem;
    display: flex;
    align-items: center;
    font-weight: 300;
    
    div {
      margin-left: 0.5rem;
    }
  }
`;

function SubjectTile({ subject }) {
  const { name } = subject;
  const mainLecturer = "Aleksander Smywiński-Pohl", isExam = true;
  return (
    <SubjectContainer variant="outlined">
      <div className="data">
        <Typography variant="h6">
          { name }
        </Typography>
        <div className="lecturer">
          <Icon name="lecturer" size="small"/>
          <div>{ mainLecturer }</div>
        </div>
      </div>
      <div className="exam">{isExam && 'E'}</div>
    </SubjectContainer>

  );
}

export default SubjectTile;
