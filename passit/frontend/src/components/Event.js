import React from "react";
import qs from "querystring";
import {IconButton} from "@material-ui/core";
import Icon from "./Icon";
import {useTranslation} from "react-i18next";
import {weekdayShorts} from "../consts/options";
import styled from "styled-components";
import {styleHelpers} from "../consts/styles";

const Container = styled.div`
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
`;

function Event({ event }) {
  const { t } = useTranslation();

  const dateTransform = date => {
    return new Date(date).toISOString().replace(/[-:]/g, "").replace(/\.\d\d\d/, "");
  };

  const query = qs.stringify({
    action: "TEMPLATE",
    dates: dateTransform(event.date) + "/" + dateTransform(event.date),
    text: event.name,
    details: event.description
  });

  const googleCalendarUrl = `https://calendar.google.com/calendar/render?${query}`;

  return (
    <Container>
      <div className="event-date">
        <div>{ t(weekdayShorts[event.weekDay]) }</div>
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
    </Container>
  );
}

export default Event;
