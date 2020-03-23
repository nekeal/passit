import React, {useEffect, useState} from 'react';
import {Container, Typography, Link, Backdrop, AppBar} from '@material-ui/core';
import styled from "styled-components";
import {BottomBar, TopBar, News, Icon, NewsEdit} from "../components";
import {authService, newsService} from "../services";
import { Link as RouterLink } from 'react-router-dom';
import {USER_TYPES} from "../consts/options";

const DashboardContainer = styled(Container)`
  padding-bottom: 5rem;
  
  .calendar-link {
    background: linear-gradient(#fff, #fff), linear-gradient(90deg, rgba(135,18,154,0.6) 40%, rgba(9,83,159,0.6) 100%);
    background-repeat: no-repeat;
    background-origin: padding-box,border-box;
    border: 2px solid transparent;
    padding: 0.7rem 1rem;
    margin-top: 1.5rem;
    box-shadow: 0 4px 4px #C8CCD6;
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
  }
`;

function Dashboard() {
  const [ newses, setNewses ] = useState([]);
  const [ sags, setSags ] = useState([]);
  const [ profileInfo, setProfileInfo ] = useState(undefined);
  const [ newsEditOpen, setNewsEditOpen ] = useState(false);
  const [ newsToUpdate, setNewsToUpdate ] = useState(undefined);
  const [ defaultFag, setDefaultFag ] = useState(undefined);

  useEffect(() => {
    authService.profileInfo()
      .then(info => {
        setProfileInfo(info);
        setDefaultFag(info.defaultFag);
        const { id } = info.defaultFag;
        return Promise.all([
          newsService.getNews(id),
          newsService.getSags(id)
        ]);
      })
      .then(([newses, sags]) => {
        setNewses(newses);
        setSags(sags);
      });

  }, []);

  useEffect(() => {
    if(defaultFag) {
      newsService.getSags(defaultFag.id).then(sags => setSags(sags));
      newsService.getNews(defaultFag.id).then(newses => setNewses(newses));
    }
  }, [defaultFag]);

  const handleAdd = news => newsService.addNews(news).then(addedNews => {
    newses.unshift(addedNews);
    setNewses(newses);
    setNewsEditOpen(false);
  });

  const handleUpdateInit = news => {
    setNewsToUpdate(news);
    setNewsEditOpen(true);
  };

  const handleUpdateConfirm = news => newsService.updateNews({id: newsToUpdate.id, ...news}).then(updatedNews => {
    setNewses(newses.map(news => news.id === updatedNews.id ? updatedNews : news));
    setNewsEditOpen(false);
  });

  const handleDelete = id => newsService.deleteNews(id).then(() => setNewses(newses.filter(ann => ann.id !== id)));

  return (
    <>
      <TopBar title="Główna" onFagChange={fag => setDefaultFag(fag)}/>
      <DashboardContainer>
        <Link component={RouterLink} to="/events" className="calendar-link">Kalendarz zaliczeń</Link>
        <div className="announcement-header">
          <Typography variant="h6" >Ogłoszenia</Typography>
          <Icon name="add" size="big" onClick={() => setNewsEditOpen(true)}/>
        </div>
        { profileInfo && newses && newses.map(news => {
          const { type } = profileInfo.defaultFag;
          const canEdit = type === USER_TYPES.REPRESENTATIVE || type === USER_TYPES.MODERATOR || news.isOwner;
          return <News key={news.id} sags={sags} news={news} canEdit={canEdit} onEdit={handleUpdateInit} onDelete={handleDelete}/>;
        })}
      </DashboardContainer>
      <BottomBar/>
      <Backdrop open={newsEditOpen} style={{zIndex: 1100}} onClick={() => setNewsEditOpen(false)}>
        { newsEditOpen && (
          newsToUpdate ?
          <NewsEdit onClose={() => setNewsEditOpen(false)} onAdd={handleUpdateConfirm} sags={sags} news={newsToUpdate}/> :
          <NewsEdit onClose={() => setNewsEditOpen(false)} onAdd={handleAdd} sags={sags}/>
        )}
      </Backdrop>
    </>
  );
}

export default Dashboard;
