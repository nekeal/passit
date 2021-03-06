import React, {useEffect, useReducer} from 'react';
import {Container, Link, Select, MenuItem, FormControl, useMediaQuery} from '@material-ui/core';
import styled from "styled-components";
import {BottomBar, SubjectTile, TopBar} from "../components";
import {subjectsService, localStorageService, authService, newsService} from "../services";
import { Link as RouterLink } from 'react-router-dom';
import { SEMESTERS } from "../consts/options";
import {useTranslation} from "react-i18next";

const SubjectsContainer = styled(Container)`
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-bottom: 5rem;
  max-width: 600px !important;
  
  .semester-select {
    margin: 1rem 0;
  }
`;

const initialState = {
  defaultFag: undefined,
  semester: localStorageService.getSemester() || 1,
  subjects: []
};

function reducer(state, action) {
  const { type, payload } = action;
  switch (type) {
    case 'SET_DEFAULT_FAG':
      return { ...state, defaultFag: payload };
    case 'SET_SEMESTER':
      return { ...state, semester: payload };
    case 'SET_SUBJECTS':
      return { ...state, subjects: payload };
    default:
      return { ...state };
  }
}

function Subjects() {
  const [ state, dispatch ] = useReducer(reducer, initialState);
  const { t } = useTranslation();
  const desktopView = useMediaQuery("(min-width:800px)");

  const { subjects, semester, defaultFag } = state;

  useEffect(() => {
    authService.profileInfo().then(({ defaultFag }) => dispatch({ type: 'SET_DEFAULT_FAG', payload: defaultFag }));
  }, []);

  useEffect(() => {
    if(defaultFag) {
      subjectsService.getSubjects(semester, defaultFag.fieldOfStudyId).then((subjects) => dispatch({ type: 'SET_SUBJECTS', payload: subjects }));
      localStorageService.setSemester(semester);
    }
  }, [semester, defaultFag]);

  return (
    <>
      <TopBar desktopView={desktopView} title={t("SUBJECTS")} onFagChange={fag => dispatch({ type: 'SET_DEFAULT_FAG', payload: fag })}/>
      <SubjectsContainer>
        <FormControl variant="outlined" className="semester-select">
          <Select id="semester" value={semester} onChange={e => dispatch({type: 'SET_SEMESTER', payload: e.target.value })}>
            {
              SEMESTERS.map(semester =>
                <MenuItem value={semester} key={semester}>Semestr {semester}</MenuItem>
              )
            }
          </Select>
        </FormControl>
        { subjects && subjects.map(subject =>
          <Link component={RouterLink} to={`/subjects/${subject.id}`} key={subject.id}>
            <SubjectTile subject={subject}/>
          </Link>
        )}
      </SubjectsContainer>
      {
        !desktopView && <BottomBar/>
      }
    </>
  );
}

export default Subjects;
