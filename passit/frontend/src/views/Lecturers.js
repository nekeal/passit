import React, { useEffect, useReducer } from 'react';
import {Container, useMediaQuery} from '@material-ui/core';
import styled from 'styled-components';
import { BottomBar, TopBar } from "../components";
import { useTranslation } from "react-i18next";
import { lecturersService } from "../services";
import { LecturerTile } from "../components";

const LecturersContainer = styled(Container)`
  margin: 1rem 0;
  
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const initialState = {
  lecturers: []
};

function reducer(state, action) {
  const { type, payload } = action;
  switch (type) {
    case 'SET_LECTURERS':
      return { ...state, lecturers: payload }
  }
}

function Lecturers() {
  const [ state, dispatch ] = useReducer(reducer, initialState);
  const desktopView = useMediaQuery("(min-width:800px)");
  const { t } = useTranslation();

  const { lecturers } = state;

  useEffect(() => {
    lecturersService.getLecturers().then(lecturers => dispatch({ type: 'SET_LECTURERS', payload: lecturers }));
  }, []);

  return (
    <>
      <TopBar desktopView={desktopView} title={t("LECTURERS")}/>
      <LecturersContainer>
        {
          lecturers.map(lecturer => <LecturerTile key={lecturer.id} lecturer={lecturer}/> )
        }
      </LecturersContainer>
      {
        !desktopView && <BottomBar/>
      }
    </>
  )
}

export default Lecturers;
