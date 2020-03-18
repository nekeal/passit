import React, {useEffect, useState} from 'react';
import { Container, Typography, Link } from '@material-ui/core';
import styled from "styled-components";
import {BottomBar, TopBar, Announcement} from "../components";
import { newsService } from "../services";
import { Link as RouterLink } from 'react-router-dom';

const DashboardContainer = styled(Container)`
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
  }
`;

function Dashboard() {
  const [ announcements, setAnnouncements ] = useState([]);

  useEffect(() => {
    newsService.getNews().then((news) => setAnnouncements(news));
  }, []);

  return (
    <>
      <TopBar title="Główna"/>
      <DashboardContainer>
        <Link component={RouterLink} to="/events" className="calendar-link">Kalendarz zaliczeń</Link>
        <Typography variant="h6" className="announcement-header">Ogłoszenia</Typography>
        { announcements && announcements.map(announcement => <Announcement key={announcement.id}  announcement={announcement}/>) }
      </DashboardContainer>
      <BottomBar/>
    </>
  );
}

export default Dashboard;
