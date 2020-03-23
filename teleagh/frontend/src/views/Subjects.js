import React, {useEffect, useState} from 'react';
import { Container, Link, Select, MenuItem, FormControl } from '@material-ui/core';
import styled from "styled-components";
import {BottomBar, SubjectTile, TopBar} from "../components";
import {subjectsService, localStorageService, authService, newsService} from "../services";
import { Link as RouterLink } from 'react-router-dom';
import { SEMESTERS } from "../consts/options";

const SubjectsContainer = styled(Container)`
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-bottom: 5rem;
  
  .semester-select {
    margin: 1rem 0;
  }
`;

function Subjects() {
  const [ subjects, setSubjects ] = useState([]);
  const [ semester, setSemester ] = useState(localStorageService.getSemester() || 1);
  const [ defaultFag, setDefaultFag ] = useState(undefined);

  useEffect(() => {
    authService.profileInfo().then(({ defaultFag }) => setDefaultFag(defaultFag));
  }, []);

  useEffect(() => {
    if(defaultFag) {
      subjectsService.getSubjects(semester, defaultFag.fieldOfStudyId).then((subjects) => setSubjects(subjects));
      localStorageService.setSemester(semester);
    }
  }, [semester, defaultFag]);

  return (
    <>
      <TopBar title="Przedmioty" onFagChange={fag => setDefaultFag(fag)}/>
      <SubjectsContainer>
        <FormControl variant="outlined" className="semester-select">
          <Select id="semester" value={semester} onChange={e => setSemester(e.target.value)}>
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
      <BottomBar/>
    </>
  );
}

export default Subjects;
