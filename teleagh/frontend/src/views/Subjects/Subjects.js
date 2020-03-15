import React, {useEffect, useState} from 'react';
import { Container, Typography, Link, InputLabel, Select, MenuItem, FormControl, Paper } from '@material-ui/core';
import styled from "styled-components";
import {BottomBar, SubjectTile, TopBar} from "../../components";
import { subjectsService } from "../../services";
import { Link as RouterLink } from 'react-router-dom';

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
  const [ semester, setSemester ] = useState(1);
  console.log(subjects);

  useEffect(() => {
    subjectsService.getSubjects(semester).then((subjects) => setSubjects(subjects));
  }, [semester]);

  return (
    <>
      <TopBar/>
      <SubjectsContainer>
        <FormControl variant="outlined" className="semester-select">
          <Select id="semester" value={semester} onChange={e => setSemester(e.target.value)}>
            {
              [1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(semester =>
                <MenuItem value={semester}>Semestr {semester}</MenuItem>
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
