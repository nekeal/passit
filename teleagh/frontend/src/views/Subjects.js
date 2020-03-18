import React, {useEffect, useState} from 'react';
import { Container, Link, Select, MenuItem, FormControl } from '@material-ui/core';
import styled from "styled-components";
import {BottomBar, SubjectTile, TopBar} from "../components";
import { subjectsService, localStorageService } from "../services";
import { Link as RouterLink } from 'react-router-dom';
import { SEMESTERS } from "../helpers/options";

const SubjectsContainer = styled(Container)`
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-bottom: 4rem;
  
  .semester-select {
    margin: 1rem 0;
  }
`;

function Subjects() {
  const [ subjects, setSubjects ] = useState([]);
  const [ semester, setSemester ] = useState(localStorageService.getSemester() || 1);

  useEffect(() => {
    subjectsService.getSubjects(semester).then((subjects) => setSubjects(subjects));
    localStorageService.setSemester(semester);
  }, [semester]);

  return (
    <>
      <TopBar title="Przedmioty"/>
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
