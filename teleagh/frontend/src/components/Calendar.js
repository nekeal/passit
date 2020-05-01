import React, {useEffect, useState} from 'react';
import {Container, Typography, IconButton} from '@material-ui/core';
import styled from "styled-components";
import {BottomBar, TopBar} from "../components";
import { eventsService } from "../services";
import { styleHelpers } from "../consts/styles";
import qs from "querystring";
import Icon from "./Icon";

const EventsContainer = styled.div`  
  padding-bottom: 5rem;
  
  .month {
    margin: 0.5rem 0;
    font-weight: 400;
  }
  
  .event {
    display: flex;
    justify-content: space-between;
    margin-bottom: 1rem;
    
    .event-date {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;  
      color: #87129A;
      font-size: 1.3rem;
      font-weight: 300;
      width: 20%;
    }
    
    .event-calendar {
      padding: 0;
    }
    
    .event-tile {
      ${styleHelpers.gradientBorder};
      border-width: 1px;
      width: 80%;
      padding: 1rem;
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      //min-height: 5rem;
    }
    
    .event-name {
      font-weight: 500;
      margin-bottom: 0.3rem;
    }
    
    .event-description {
      font-weight: 300;
      margin-bottom: 0.3rem;
    }
    
    .event-time {
      font-weight: 300;
    }
  }
`;

const monthNames = ["Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec", "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień"];

const weekdayShorts = ["pon.", "wt.", "śr.", "czw.", "pt.", "sb.", "nd."];

function Calendar({ eventsByMonths }) {

  const dateTransform = date => {
    return new Date(date).toISOString().replace(/[-:]/g, "").replace(/\.\d\d\d/, "");
  };

  const renderEvent = event => {

    const query = qs.stringify({
      action: "TEMPLATE",
      dates: dateTransform(event.date) + "/" + dateTransform(event.date),
      text: event.name,
      details: event.description
    });

    const googleCalendarUrl = `https://calendar.google.com/calendar/render?${query}`;

    return (
      <div className="event" key={event.id}>
        <div className="event-date">
          <div>{ weekdayShorts[event.weekDay] }</div>
          <div>{ event.monthDay }</div>
        </div>
        <div className="event-tile">
          <div className="event-data">
            <div className="event-name">{ event.name }</div>
            <div className="event-description">{ event.description }</div>
            <div className="event-time">{ event.time }</div>
          </div>
          <IconButton className="event-calendar" href={googleCalendarUrl} target="_blank" rel="noreferrer noopener">
            <Icon name="calendar" clickable/>
          </IconButton>
        </div>
      </div>
    );
  };

  return (
    <EventsContainer>
      {
        eventsByMonths && eventsByMonths.map(monthEvents =>
          <div key={monthEvents.month}>
            <Typography className="month" variant="h5">{ monthNames[monthEvents.month] }</Typography>
            { monthEvents.events.map(renderEvent) }
          </div>
        )
      }
    </EventsContainer>
  );
}

export default Calendar;
