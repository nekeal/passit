import React, {useEffect, useState} from 'react';
import {Container, Typography} from '@material-ui/core';
import styled from "styled-components";
import {BottomBar, TopBar} from "../components";
import { eventsService } from "../services";
import styleHelpers from "../consts/styles";


const EventsContainer = styled(Container)`  
  margin-top: 1rem;
  
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
    
    .event-tile {
      ${styleHelpers.gradientBorder};
      border-width: 1px;
      width: 80%;
      padding: 1rem;
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

function Events() {
  const [ eventsByMonths, setEventsByMonths ] = useState([]);
  console.log(eventsByMonths);

  useEffect(() => {
    eventsService.getEvents().then(eventsByMonths => setEventsByMonths(eventsByMonths));
  }, []);

  return (
    <>
      <TopBar title="Kalendarz zaliczeń"/>
      <EventsContainer>
        {
          eventsByMonths && eventsByMonths.map(monthEvents =>
            <>
              <Typography className="month" variant="h5">{ monthNames[monthEvents.month] }</Typography>
              { monthEvents.events.map(event =>
                <div className="event">
                  <div className="event-date">
                    <div>{ weekdayShorts[event.weekDay] }</div>
                    <div>{ event.monthDay }</div>
                  </div>
                  <div className="event-tile">
                    <div className="event-name">{ event.name }</div>
                    <div className="event-description">{ event.description }</div>
                    <div className="event-time">{ event.time }</div>
                  </div>
                </div>
              ) }
            </>
          )
        }
      </EventsContainer>
      <BottomBar/>
    </>
  );
}

export default Events;
