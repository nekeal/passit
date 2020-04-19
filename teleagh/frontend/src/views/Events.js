import React, {useEffect, useState} from 'react';
import {Container, Typography} from '@material-ui/core';
import styled from "styled-components";
import {BottomBar, Calendar, TopBar} from "../components";
import { eventsService } from "../services";
import styleHelpers from "../consts/styles";

function Events() {
  const [ eventsByMonths, setEventsByMonths ] = useState([]);

  useEffect(() => {
    eventsService.getEvents().then(eventsByMonths => setEventsByMonths(eventsByMonths));
  }, []);

  return (
    <>
      <TopBar title="Kalendarz zaliczeń" allowBack/>
      <Calendar eventsByMonths={eventsByMonths}/>
      <BottomBar/>
    </>
  );
}

export default Events;
