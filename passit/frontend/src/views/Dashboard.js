import React, {useEffect, useReducer} from 'react';
import {Container, Typography, Link, Backdrop, useMediaQuery} from '@material-ui/core';
import styled from "styled-components";
import {BottomBar, TopBar, NewsEdit, ConfirmationDialog, Loader, Calendar} from "../components";
import {authService, eventsService, newsService} from "../services";
import { Link as RouterLink } from 'react-router-dom';
import {SNACKBAR_TYPES} from "../consts/options";
import { styleHelpers } from "../consts/styles";
import {useTranslation} from "react-i18next";
import NewsList from "../components/NewsList";

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
  
  .dashboard-items {
    margin-top: 2rem;
    display: flex;
    justify-content: space-between;
  }
  
  
  .calendar {
    width: 45%;
    padding: 1rem;
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
  displayedNewses: []
};

const filterNewses = (newses, searchText) => {
  searchText = searchText.toUpperCase();
  return newses.filter(news => news.title.toUpperCase().includes(searchText) || news.content.toUpperCase().includes(searchText) || news.author.toUpperCase().includes(searchText));
};

function reducer(state, action) {
  const { type, payload } = action;
  switch (type) {
    case 'SET_PROFILE_INFO':
      return { ...state, profileInfo: payload };
    case 'SET_DATA':
      const { newses, sags } = payload;
      return { ...state, newses, displayedNewses: newses, sags, initialized: true };
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
    case 'NEWS_SEARCH_RESET':
      return { ...state, displayedNewses: state.newses };
    case 'NEWS_SEARCH_CHANGE':
      return { ...state, displayedNewses: filterNewses(state.newses, payload) };
    default:
      return { ...state };
  }
}

function Dashboard({ setSnackbar }) {
  const [state, dispatch] = useReducer(reducer, initialState);
  const { t } = useTranslation();
  const desktopView = useMediaQuery("(min-width:800px)");

  const { initialized, profileInfo, sags, processedNews, newsEditOpen, newsDeleteOpen, displayedNewses } = state;

  useEffect(() => {
    authService.profileInfo()
      .then(info => {
        dispatch({ type: 'SET_PROFILE_INFO', payload: info });
        const { id } = info.defaultFag;
        const promises = [newsService.getNews(id), newsService.getSags(id)];
        return Promise.all(promises);
      })
      .then(([newses, sags]) => {
        dispatch({ type: 'SET_DATA', payload: { newses, sags }});
      });

  }, []);

  useEffect(() => {
    if(initialized) {
      const { defaultFag: { id } } = profileInfo;
      const promises = [newsService.getNews(id), newsService.getSags(id)];
      Promise.all(promises).then(([newses, sags]) => {
        dispatch({ type: 'SET_DATA', payload: { newses, sags }});
      });
    }
  }, [profileInfo]);

  const handleAddNews = news =>
    newsService
      .addNews(news)
      .then(addedNews => {
        setSnackbar(SNACKBAR_TYPES.SUCCESS, t("NEWS_ADDED_SUCCESSFULLY"));
        dispatch({ type: 'NEWS_EDIT_ACCEPT', payload: addedNews })
      });

  const handleUpdateNews = news =>
    newsService
      .updateNews({id: processedNews.id, ...news})
      .then(updatedNews => {
        setSnackbar(SNACKBAR_TYPES.SUCCESS, t("NEWS_UPDATED_SUCCESSFULLY"));
        dispatch({ type: 'NEWS_EDIT_ACCEPT', payload: updatedNews })
      });

  const handleDeleteNews = () =>
    newsService
      .deleteNews(processedNews.id)
      .then(() => {
        setSnackbar(SNACKBAR_TYPES.SUCCESS, t("NEWS_DELETED_SUCCESSFULLY"));
        dispatch({ type: "NEWS_DELETE_ACCEPT"});
      })
      .catch(() => {
        setSnackbar(SNACKBAR_TYPES.ERROR, t("NEWS_DELETE_ERROR"));
        dispatch({ type: "NEWS_DELETE_DECLINE"});
      });

  return (
    <>
      <TopBar desktopView={desktopView} title={t("DASHBOARD")} onFagChange={fag => dispatch({ type: 'CHANGE_DEFAULT_FAG', payload: fag })}/>
      {
        initialized ? (
          <DashboardContainer>
            {
              !desktopView && <Link component={RouterLink} to="/events" className="calendar-link">{t("ASSIGNMENTS_CALENDAR")}</Link>
            }
            <div className="dashboard-items">
              <NewsList
                newses={displayedNewses}
                sags={sags}
                profileInfo={profileInfo}
                onSearchReset={() => dispatch({ type: 'NEWS_SEARCH_RESET'})}
                onSearchChange={text => dispatch({ type: "NEWS_SEARCH_CHANGE", payload: text })}
                onNewsAdd={() => dispatch({ type: 'NEWS_ADD_INIT'})}
                onNewsEdit={news => dispatch({type: 'NEWS_EDIT_INIT', payload: news })}
                onNewsDelete={news => dispatch({type: 'NEWS_DELETE_INIT', payload: news})}
              />
              {
                desktopView &&
                  <div className="calendar">
                    <Calendar/>
                  </div>
              }
            </div>
          </DashboardContainer>
        ) : (
          <Loader desktopView={desktopView}/>
        )
      }
      {
        !desktopView && <BottomBar/>
      }
      <Backdrop open={newsEditOpen} style={{zIndex: 1100}}>
        { newsEditOpen && (
          <NewsEdit
            onAccept={processedNews ? handleUpdateNews : handleAddNews}
            onDecline={() => dispatch({ type: 'NEWS_EDIT_DECLINE' })}
            sags={sags}
            news={processedNews}
          />
        )}
      </Backdrop>
      <ConfirmationDialog open={newsDeleteOpen} onAccept={handleDeleteNews} onDecline={() => dispatch({ type: 'NEWS_DELETE_DECLINE' })}/>
    </>
  );
}

export default Dashboard;
