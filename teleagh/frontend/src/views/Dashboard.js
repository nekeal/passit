import React, {useEffect, useReducer} from 'react';
import {Container, Typography, Link, Backdrop, Input, IconButton, InputAdornment} from '@material-ui/core';
import styled from "styled-components";
import {BottomBar, TopBar, News, Icon, NewsEdit, ConfirmationDialog} from "../components";
import {authService, newsService} from "../services";
import { Link as RouterLink } from 'react-router-dom';
import {USER_TYPES} from "../consts/options";
import styleHelpers from "../consts/styles";
import {useTranslation} from "react-i18next";

const DashboardContainer = styled(Container)`
  padding-bottom: 5rem;
  
  .calendar-link {
    ${styleHelpers.gradientBorder};
    padding: 0.7rem 1rem;
    margin-top: 1.5rem;
    color: inherit;
    display: block;
    text-decoration: none;
  }
  
  
  .announcement-header {
    margin-top: 2rem;
    margin-bottom: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    img {
      margin-left: 0.8rem;
    }
    
    .news-search {
      ${styleHelpers.gradientBorder};
      padding: 0.2rem;
      width: 100%;
      
      .MuiIconButton-root {
        padding: 0;
      }
      
      img {
        margin: 0 0.4rem;
      }
    }
  }
`;

const initialState = {
  initialized: false,
  profileInfo: undefined,
  newses: [],
  sags: [],
  processedNews: undefined,
  newsEditOpen: false,
  newsDeleteOpen: false,
  newsSearchOpen: false,
  searchText: "",
  displayedNewses: []
};

const filterNewses = (newses, searchText) => {
  searchText = searchText.toUpperCase();
  return newses.filter(news => news.title.toUpperCase().includes(searchText) || news.content.toUpperCase().includes(searchText) || news.author.includes(searchText));
};

function reducer(state, action) {
  const { type, payload } = action;
  switch (type) {
    case 'SET_PROFILE_INFO':
      return { ...state, profileInfo: payload };
    case 'SET_DATA':
      return { ...state, newses: payload.newses, sags: payload.sags, initialized: true };
    case 'CHANGE_DEFAULT_FAG':
      return { ...state, profileInfo: { ...state.profileInfo, defaultFag: payload }};
    case 'NEWS_ADD_INIT':
      return { ...state, newsEditOpen: true };
    case 'NEWS_EDIT_INIT':
      return { ...state, newsEditOpen: true, processedNews: payload };
    case 'NEWS_EDIT_ACCEPT':
      if(state.processedNews) {
        return { ...state, newsEditOpen: false, processedNews: undefined, newses: state.newses.map(news => news.id === state.processedNews.id ? payload : news) }
      } else {
        return { ...state, newsEditOpen: false, newses: [ payload, ...state.newses ] }
      }
    case 'NEWS_EDIT_DECLINE':
      return { ...state, newsEditOpen: false, processedNews: undefined };
    case 'NEWS_DELETE_INIT':
      return { ...state, newsDeleteOpen: true, processedNews: payload };
    case 'NEWS_DELETE_ACCEPT':
      return { ...state, newsDeleteOpen: false, processedNews: undefined,  newses: state.newses.filter(news => news.id !== state.processedNews.id) };
    case 'NEWS_DELETE_DECLINE':
      return { ...state, newsDeleteOpen: false, processedNews: undefined };
    case 'NEWS_SEARCH_INIT':
      return { ...state, newsSearchOpen: true, displayedNewses: state.newses };
    case 'NEWS_SEARCH_CHANGE':
      return { ...state, searchText: payload, displayedNewses: filterNewses(state.newses, payload) };
    case 'NEWS_SEARCH_END':
      return { ...state, searchText: "", newsSearchOpen: false };
  }
}

function Dashboard() {
  const [state, dispatch] = useReducer(reducer, initialState);
  const { t } = useTranslation();

  const { initialized, profileInfo, newses, sags, processedNews, newsEditOpen, newsDeleteOpen, newsSearchOpen, searchText, displayedNewses } = state;

  useEffect(() => {
    authService.profileInfo()
      .then(info => {
        dispatch({ type: 'SET_PROFILE_INFO', payload: info });
        const { id } = info.defaultFag;
        return Promise.all([
          newsService.getNews(id),
          newsService.getSags(id)
        ]);
      })
      .then(([newses, sags]) => {
        dispatch({ type: 'SET_DATA', payload: { newses, sags }});
      });

  }, []);

  useEffect(() => {
    if(initialized) {
      const { defaultFag: { id } } = profileInfo;
      Promise.all([
        newsService.getNews(id),
        newsService.getSags(id)
      ]).then(([newses, sags]) => {
        dispatch({ type: 'SET_DATA', payload: { newses, sags }});
      });
    }
  }, [profileInfo]);

  const handleAdd = news => newsService.addNews(news).then(addedNews => dispatch({ type: 'NEWS_EDIT_ACCEPT', payload: addedNews }));

  const handleUpdate = news =>
    newsService.updateNews({id: processedNews.id, ...news}).then(updatedNews => dispatch({ type: 'NEWS_EDIT_ACCEPT', payload: updatedNews }));

  const handleDelete = () => newsService.deleteNews(processedNews.id).then(() => dispatch({ type: 'NEWS_DELETE_ACCEPT'}));

  const mapNewses = newses => newses.map(news => {
    const { type } = profileInfo.defaultFag;
    const canEdit = type === USER_TYPES.REPRESENTATIVE || type === USER_TYPES.MODERATOR || news.isOwner;
    return <News
      key={news.id}
      sags={sags}
      news={news}
      canEdit={canEdit}
      onEdit={() => dispatch({type: 'NEWS_EDIT_INIT', payload: news })}
      onDelete={() => dispatch({type: 'NEWS_DELETE_INIT', payload: news})}
    />;
  });

  return (
    <>
      <TopBar title={t("DASHBOARD")} onFagChange={fag => dispatch({ type: 'CHANGE_DEFAULT_FAG', payload: fag })}/>
      <DashboardContainer>
        <Link component={RouterLink} to="/events" className="calendar-link">{t("ASSIGNMENTS_CALENDAR")}</Link>
        {
          newsSearchOpen ? (
            <>
              <div className="announcement-header">
                <Input
                  className="news-search"
                  value={searchText}
                  onChange={e => dispatch({ type: "NEWS_SEARCH_CHANGE", payload: e.target.value })}
                  placeholder="Słowo klucz, imię lub nazwisko"
                  startAdornment={
                    <Icon name="search"/>
                  }
                  endAdornment={
                    <InputAdornment position="end">
                      <IconButton onClick={() => dispatch({ type: "NEWS_SEARCH_END"})}>
                        <Icon name="decline"/>
                      </IconButton>
                    </InputAdornment>
                  }
                />
              </div>
              { profileInfo && newses && mapNewses(displayedNewses)}
            </>
          ) : (
            <>
              <div className="announcement-header">
                <Typography variant="h6" >{t("ANNOUNCEMENTS")}</Typography>
                <div>
                  <Icon name="search" size="big" onClick={() => dispatch({ type: 'NEWS_SEARCH_INIT'})}/>
                  <Icon name="add" size="big" onClick={() => dispatch({ type: 'NEWS_ADD_INIT'})}/>
                </div>
              </div>
              { profileInfo && newses && mapNewses(newses)}
            </>
          )
        }
      </DashboardContainer>
      <BottomBar/>
      <Backdrop open={newsEditOpen} style={{zIndex: 1100}} onClick={() => dispatch({ type: 'NEWS_EDIT_DECLINE' })}>
        { newsEditOpen && (
          <NewsEdit
            onAccept={processedNews ? handleUpdate : handleAdd}
            onDecline={() => dispatch({ type: 'NEWS_EDIT_DECLINE' })}
            sags={sags}
            news={processedNews}
          />
        )}
      </Backdrop>
      <ConfirmationDialog open={newsDeleteOpen} onAccept={handleDelete} onDecline={() => dispatch({ type: 'NEWS_DELETE_DECLINE' })}/>
    </>
  );
}

export default Dashboard;
