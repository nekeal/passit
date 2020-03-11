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
            <MenuItem value={1}>Semestr 1</MenuItem>
            <MenuItem value={2}>Semestr 2</MenuItem>
            <MenuItem value={3}>Semestr 3</MenuItem>
            <MenuItem value={4}>Semestr 4</MenuItem>
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
