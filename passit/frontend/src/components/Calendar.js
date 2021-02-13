import React, {useEffect, useReducer} from 'react';
import {Typography} from '@material-ui/core';
import styled from "styled-components";
import { styleHelpers } from "../consts/styles";
import Icon from "./Icon";
import {useTranslation} from "react-i18next";
import {eventsService} from "../services";
import Event from "./Event";
import {monthNames} from "../consts/options";

const EventsContainer = styled.div`  
  padding-bottom: 5rem;
  
  .events-header {
    display: flex;
    justify-content: space-between;
  }
  
  .month {
    margin: 0.5rem 0;
    font-weight: 400;
  }
`;


const initialState = {
  eventsByMonths: []
};

function reducer(state, action) {
  const { type, payload } = action;
  switch (type) {
    case "SET_EVENTS":
      return { ...state, eventsByMonths: payload };
    default:
      return { ...state };
  }
}

function Calendar() {
  const { t } = useTranslation();
  const [ state, dispatch ] = useReducer(reducer, initialState);

  useEffect(() => {
    eventsService.getEvents().then(eventsByMonths => dispatch({ type: "SET_EVENTS", payload: eventsByMonths }));
  }, []);

  const { eventsByMonths } = state;


  // const renderEvent = event => {
  //
  //   const query = qs.stringify({
  //     action: "TEMPLATE",
  //     dates: dateTransform(event.date) + "/" + dateTransform(event.date),
  //     text: event.name,
  //     details: event.description
  //   });
  //
  //   const googleCalendarUrl = `https://calendar.google.com/calendar/render?${query}`;
  //
  //   return (
  //     <div className="event" key={event.id}>
  //       <div className="event-date">
  //         <div>{ t(weekdayShorts[event.weekDay]) }</div>
  //         <div>{ event.monthDay }</div>
  //       </div>
  //       <div className="event-tile">
  //         <div className="event-data">
  //           <div className="event-name">{ event.name }</div>
  //           <div className="event-description">{ event.description }</div>
  //           <div className="event-time">{ event.time }</div>
  //         </div>
  //         <IconButton className="event-calendar" href={googleCalendarUrl} target="_blank" rel="noreferrer noopener">
  //           <Icon name="calendar" clickable/>
  //         </IconButton>
  //       </div>
  //     </div>
  //   );
  // };

  return (
    <EventsContainer>
      <div className="events-header">
        <Typography variant="h6" >{t("ASSIGNMENTS_CALENDAR")}</Typography>
        <Icon name="add" size="big" clickable onClick={() => {}}/>
      </div>
      {
        eventsByMonths && eventsByMonths.map(monthEvents =>
          <div key={monthEvents.month}>
            <Typography className="month" variant="h5">{ t(monthNames[monthEvents.month]) }</Typography>
            { monthEvents.events.map(event => <Event event={event} key={event.id}/>) }
          </div>
        )
      }
    </EventsContainer>
  );
}

export default Calendar;
