import React, {useEffect, useState} from 'react';
import {Container, Tabs, Tab, Typography, Paper, useMediaQuery} from '@material-ui/core';
import styled from "styled-components";
import {BottomBar, Icon, TopBar} from "../components";
import { subjectsService } from "../services";
import { useParams } from "react-router-dom";
import styleHelpers from "../consts/styles";
import { RESOURCE_TYPES } from "../consts/options";

const SubjectContainer = styled(Container)`  
  .tabs {
    margin-top: 0.3rem;
  }
  
  .desktop-container {
    margin-top: 2rem;
    display: flex;
    justify-content: space-between; 
  }
  
  .desktop-general {
    & > h5 {
      margin-bottom: 1rem;
    }
  }
  
  .desktop-resources {
    & > h5 {
      margin-bottom: 1rem;
    }
  }
  
  .general-info {
    ${styleHelpers.gradientBorder};
    padding: 1rem;
    
    h5 {
      margin: 0.3rem 0;
    }
  }

  .resource-container {
     margin: 1rem 1.5rem;
     text-align: center;
     
     .resource {
        display: flex;
        align-items: center;
        justify-content: center;
        border-top: #E5E5E5 1px solid;
        padding: 0.7rem 0;
        color: #87129A;
        
        img {
          margin-right: 0.5rem;
        }
        
        div {
          padding-top: 0.2rem;
        }
     }
     
     a:last-child .resource {
        border-bottom: #E5E5E5 1px solid;
     }
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
  const [ tabIndex, setTabIndex ] = useState(0);
  const [ resourcesTabIndex, setResourcesTabIndex ] = useState(0);
  const [ resources, setResources ] = useState({});
  const desktopView = useMediaQuery("(min-width:800px)");

  useEffect(() => {
    console.log(desktopView);
    subjectsService.getSubject(params.id).then((subject) => setSubject(subject));
  }, [params.id]);

  useEffect(() => {
    if(tabIndex === 1) {
      subjectsService.getResources(params.id, RESOURCE_TYPES[resourcesTabIndex]).then((categoryResources) => {
        const newResources = { ...resources };
        newResources[RESOURCE_TYPES[resourcesTabIndex]] = categoryResources;
        setResources(newResources);
      });
    }
  }, [params.id, tabIndex, resourcesTabIndex]);

  const renderGeneral = () => <>
    <Typography variant="h5">Ogólne</Typography>
    <Paper className="general-info">
      <Typography variant="h5">Prowadzący:</Typography>
      <Typography variant="h6">obecnie</Typography>
      <div className="lecturer">
        <span className="name">dr hab. Andrzej Rusek</span>
        <span className="function">wykładowca, prowadzący</span>
      </div>
    </Paper>
    <Typography variant="h5">Opinie</Typography>
  </>;

  const renderResources = () => <>
    <Tabs value={resourcesTabIndex} onChange={(e, newValue) => setResourcesTabIndex(newValue)} centered className="tabs">
      <Tab label="Wykłady"/>
      <Tab label="Egzaminy"/>
      <Tab label="Kolokwia"/>
      <Tab label="Inne"/>
    </Tabs>
    {
      RESOURCE_TYPES.map((category, index) =>
        <TabPanel value={resourcesTabIndex} key={index} index={index} className="resource-container">
          { resources[category] && resources[category].length ? resources[category].map(resource =>
            <a href={resource.url} key={resource.id} target="_blank" rel="noopener noreferrer">
              <div className="resource">
                <Icon name={resource.type}/>
                <div>{ resource.name }</div>
              </div>
            </a>
          ) : "Brak materiałów z tej kategorii"}
        </TabPanel>
      )
    }
  </>;

  return (
    <>
      <TopBar desktopView={desktopView} title={subject && subject.name} allowBack />
      <SubjectContainer>
        {
          desktopView ? (
            <div className="desktop-container">
              <div className="desktop-general">
                <Typography variant="h5">Opis</Typography>
                { renderGeneral() }
              </div>
              <div className="desktop-resources">
                <Typography variant="h5">Materiały</Typography>
                { renderResources() }
              </div>
            </div>
          ) : (
            <>
              <Tabs value={tabIndex} onChange={(e, newValue) => setTabIndex(newValue)} centered className="tabs">
                <Tab label="Opis"/>
                <Tab label="Materiały"/>
              </Tabs>
              <TabPanel value={tabIndex} index={0}>
                { renderGeneral() }
              </TabPanel>
              <TabPanel value={tabIndex} index={1}>
                { renderResources() }
              </TabPanel>
            </>
          )
        }
      </SubjectContainer>
      {
        !desktopView && <BottomBar/>
      }
    </>
  );
}

export default Subject;
