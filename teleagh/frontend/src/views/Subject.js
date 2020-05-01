import React, {useEffect, useReducer, useState} from 'react';
import {Container, Tabs, Tab, Typography, Paper, useMediaQuery, Backdrop} from '@material-ui/core';
import styled from "styled-components";
import {BottomBar, ConfirmationDialog, Icon, NewsEdit, Opinion, TopBar} from "../components";
import { subjectsService } from "../services";
import { useParams } from "react-router-dom";
import { styleHelpers } from "../consts/styles";
import { RESOURCE_TYPES } from "../consts/options";
import OpinionEdit from "../components/OpinionEdit";
import {APP_ROUTES} from "../consts/routes";
import { Link } from "react-router-dom";
import {useTranslation} from "react-i18next";

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
      margin: 1rem 0;
    }
    flex-basis: 40%;
    flex-shrink: 0;
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
  
  .opinion-header {
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    img {
      margin-left: 0.8rem;
    }
  }

`;

const initialState = {
  subject: {},
  opinions: [],
  resources: {},
  tabIndex: 0,
  resourcesTabIndex: 0,
  processedOpinion: undefined,
  opinionEditOpen: false,
  opinionDeleteOpen: false
};

function reducer(state, action) {
  const { type, payload } = action;
  switch (type) {
    case "SET_SUBJECT_INFO":
      return { ...state, subject: payload };
    case "SET_OPINIONS":
      return { ...state, opinions: payload };
    case "SET_RESOURCES":
      return { ...state, resources: payload };
    case "SET_TAB_INDEX":
      return { ...state, tabIndex: payload };
    case "SET_RESOURCES_TAB_INDEX":
      return { ...state, resourcesTabIndex: payload };
    case "OPINION_ADD_INIT":
      return { ...state, opinionEditOpen: true };
    case "OPINION_EDIT_INIT":
      return { ...state, opinionEditOpen: true, processedOpinion: payload };
    case "OPINION_EDIT_ACCEPT":
      if(state.processedOpinion) {
        return { ...state, opinionEditOpen: false, processedOpinion: undefined, opinions: state.opinions.map(opinion => opinion.id === state.processedOpinion.id ? payload : opinion) }
      } else {
        return { ...state, opinionEditOpen: false, opinions: [ payload, ...state.opinions ] }
      }
    case "OPINION_EDIT_DECLINE":
      return { ...state, opinionEditOpen: false, processedOpinion: undefined };
    case "OPINION_DELETE_INIT":
      return { ...state, opinionDeleteOpen: true, processedOpinion: payload };
    case "OPINION_DELETE_ACCEPT":
      return { ...state, opinionDeleteOpen: false, processedOpinion: undefined,  opinions: state.opinions.filter(opinion => opinion.id !== state.processedOpinion.id) };
    case "OPINION_DELETE_DECLINE":
      return { ...state, opinionDeleteOpen: false, processedOpinion: undefined };
    default:
      return { ...state };
  }
}

function Subject() {
  const params = useParams();
  const [ state, dispatch ] = useReducer(reducer, initialState);
  const desktopView = useMediaQuery("(min-width:800px)");
  const { t } = useTranslation();

  const { subject, opinions, resources, tabIndex, resourcesTabIndex, opinionEditOpen, opinionDeleteOpen, processedOpinion } = state;

  useEffect(() => {
    subjectsService.getSubject(params.id).then(subject => dispatch({ type: "SET_SUBJECT_INFO", payload: subject }));
    subjectsService.getOpinions(params.id).then(opinions => dispatch({ type: "SET_OPINIONS", payload: opinions }));
  }, [params.id]);

  useEffect(() => {
    if(tabIndex === 1 || desktopView) {
      subjectsService.getResources(params.id, RESOURCE_TYPES[resourcesTabIndex]).then((categoryResources) => {
        const newResources = { ...resources };
        newResources[RESOURCE_TYPES[resourcesTabIndex]] = categoryResources;
        dispatch({ type: "SET_RESOURCES", payload: newResources });
      });
    }
  }, [params.id, tabIndex, resourcesTabIndex, desktopView]);

  const TabPanel = ({ children, value, index, ...other }) =>
    <Typography component="div" role="tabpanel" hidden={value !== index} {...other}>
      {value === index && <>{children}</>}
    </Typography>;

  const handleAddOpinion = opinion =>
    subjectsService.addOpinion(subject.id, opinion).then(addedOpinion => dispatch({ type: "OPINION_EDIT_ACCEPT", payload: addedOpinion }));

  const handleEditOpinion = opinion =>
    subjectsService.updateOpinion({ id: processedOpinion.id, ...opinion }).then(updatedOpinion => dispatch({ type: "OPINION_EDIT_ACCEPT", payload: updatedOpinion }));

  const handleDeleteOpinion = () =>
    subjectsService.deleteOpinion(processedOpinion.id).then(() => dispatch({ type: "OPINION_DELETE_ACCEPT" }));

  const renderOpinions = () => <>
    <div className="opinion-header">
      <Typography variant="h5">{t("OPINIONS")}</Typography>
      <div>
        <Icon name="add" size="big" clickable onClick={() => dispatch({ type: 'OPINION_ADD_INIT'})}/>
      </div>
    </div>
    { opinions.map(opinion =>
      <Opinion
        opinion={opinion}
        onEdit={() => dispatch({ type: "OPINION_EDIT_INIT", payload: opinion })}
        onDelete={() => dispatch({ type: "OPINION_DELETE_INIT", payload: opinion })}
      />) }
  </>;

  const renderGeneral = () => <>
    <Typography variant="h5">{t("GENERAL")}</Typography>
    <Paper className="general-info">
      <Typography variant="h5">{t("LECTURERS")}:</Typography>
      {
        subject.lecturers && subject.lecturers.map(({ id, fullName }) =>
          <div className="lecturer">
            <Link to={APP_ROUTES.LECTURER(id)} className="name">{ fullName }</Link>
          </div>
        )
      }
    </Paper>
    { renderOpinions() }
  </>;

  const renderResources = () => <>
    <Tabs value={resourcesTabIndex} onChange={(e, newValue) => dispatch({ type: "SET_RESOURCES_TAB_INDEX", payload: newValue })} centered className="tabs">
      <Tab label={t("LECTURES")}/>
      <Tab label={t("EXAMS")}/>
      <Tab label={t("MID_TERM_EXAMS")}/>
      <Tab label={t("OTHER")}/>
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
          ) : t("NO_RESOURCES_IN_CATEGORY") }
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
                <Typography variant="h3">{ subject.name }</Typography>
                { renderGeneral() }
              </div>
              <div className="desktop-resources">
                <Typography variant="h5">{t("RESOURCES")}</Typography>
                { renderResources() }
              </div>
            </div>
          ) : (
            <>
              <Tabs value={tabIndex} onChange={(e, newValue) => dispatch({ type: "SET_TAB_INDEX", payload: newValue })} centered className="tabs">
                <Tab label="Opis"/>
                <Tab label={t("RESOURCES")}/>
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
      <Backdrop open={opinionEditOpen} style={{zIndex: 1100}}>
        { opinionEditOpen && (
          <OpinionEdit
            opinion={processedOpinion}
            onAccept={processedOpinion ? handleEditOpinion : handleAddOpinion}
            onDecline={() => dispatch({ type: 'OPINION_EDIT_DECLINE' })}
          />
        )}
      </Backdrop>
      <ConfirmationDialog open={opinionDeleteOpen} onAccept={handleDeleteOpinion} onDecline={() => dispatch({ type: 'OPINION_DELETE_DECLINE' })}/>
    </>
  );
}

export default Subject;
