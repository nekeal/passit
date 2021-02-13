import React, {useEffect, useState} from 'react';
import {BottomBar, Calendar, TopBar} from "../components";
import { eventsService } from "../services";
import styled from "styled-components";

const Container = styled.div`
    width: 90%;
    margin: 0 auto;
`;

function Events() {
  // const [ eventsByMonths, setEventsByMonths ] = useState([]);
  //
  // useEffect(() => {
  //   eventsService.getEvents().then(eventsByMonths => setEventsByMonths(eventsByMonths));
  // }, []);

  return (
    <>
      <TopBar title="Kalendarz zaliczeń" allowBack/>
        <Container>
          <Calendar/>
        </Container>
      <BottomBar/>
    </>
  );
}

export default Events;
