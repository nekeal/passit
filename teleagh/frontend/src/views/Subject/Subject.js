import React, {useEffect, useState} from 'react';
import { Container, Tabs, Tab, Typography, Paper, Link } from '@material-ui/core';
import styled from "styled-components";
import {BottomBar, TopBar} from "../../components";
import { subjectsService } from "../../services";
import { Link as RouterLink } from 'react-router-dom';
import { useParams } from "react-router-dom";
import styleHelpers from "../../helpers/styles";

const SubjectContainer = styled(Container)`  
  .tabs {
    margin-top: 0.3rem;
  }

  .resource-container {
     margin: 1rem 1.5rem;
     text-align: center;
     
     .resource {
        border-top: #E5E5E5 1px solid;
        padding: 0.7rem 0;
        color: #87129A;
     }
     
     a:last-child .resource {
        border-bottom: #E5E5E5 1px solid;
     }
  }
`;

const GeneralInfo = styled(Paper)`
  ${styleHelpers.gradientBorder};
  padding: 1rem;
  
  h5 {
    margin: 0.3rem 0;
  }
`;

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <Typography component="div" role="tabpanel" hidden={value !== index} {...other}>
      {value === index && <>{children}</>}
    </Typography>
  );
}

function Subject() {
  const params = useParams();
  const [ subject, setSubject ] = useState({});
  const [ tabIndex, setTabIndex ] = useState(1);
  const [ resourcesTabIndex, setResourcesTabIndex ] = useState(3);
  const [ resources, setResources ] = useState({});


  useEffect(() => {
    subjectsService.getSubject(params.id).then((subject) => setSubject(subject));
    subjectsService.getResources(params.id).then((resources) => setResources(resources));
  }, [params.id]);

  return (
    <>
      <TopBar/>
      <SubjectContainer>
        <Tabs value={tabIndex} onChange={(e, newValue) => setTabIndex(newValue)} centered className="tabs">
          <Tab label="Opis"/>
          <Tab label="Materiały"/>
        </Tabs>
        <TabPanel value={tabIndex} index={0}>
          <Typography variant="h5">Ogólne</Typography>
          <GeneralInfo>
            E - przedmiot objęty egzaminem
            <Typography variant="h5">Prowadzący:</Typography>
            <Typography variant="h6">obecnie</Typography>
            <div className="lecturer">
              <span className="name">dr hab. Andrzej Rusek</span>og
              <span className="function">wykładowca, prowadzący</span>
            </div>
            <Typography variant="h6">2018/2019:</Typography>
          </GeneralInfo>
          <Typography variant="h5">Opinie</Typography>
        </TabPanel>
        <TabPanel value={tabIndex} index={1}>
          <Tabs value={resourcesTabIndex} onChange={(e, newValue) => setResourcesTabIndex(newValue)} centered className="tabs">
            <Tab label="Wykłady"/>
            <Tab label="Egzaminy"/>
            <Tab label="Kolokwia"/>
            <Tab label="Inne"/>
          </Tabs>
          {
            ["LECTURE", "EXAM", "MID_TERM_EXAM", "OTHER"].map((category, index) =>
              <TabPanel value={resourcesTabIndex} key={index} index={index} className="resource-container">
                { resources[category] && resources[category].length ? resources[category].map(resource =>
                  <a href={resource.url} key={resource.id} target="_blank">
                    <div className="resource">
                      { resource.name }
                    </div>
                  </a>
                ) : "Nie ma jeszcze materiałów :("}
              </TabPanel>
            )
          }
        </TabPanel>
      </SubjectContainer>
      <BottomBar/>
    </>
  );
}

export default Subject;
