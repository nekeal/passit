import axios from "axios";
import { API_ROUTES } from "../consts/routes";


function formatTime(date) {
  return `${date.getHours()}:${("0" + date.getMinutes()).slice(-2)}`;
}

function getEvents() {
  return axios
    .get(API_ROUTES.EVENTS)
    .then(response => {
      // console.log(response.data.sort((a, b) => new Date(a.due_date) - new Date(b.due_date)));
      return response.data
        .sort((a, b) => new Date(a.due_date) - new Date(b.due_date))
        .reduce((eventsByMonth, event) => {
          const { name, description, category, due_date } = event;
          const date = new Date(due_date);
          const month = date.getMonth();

          let monthEvents = eventsByMonth[eventsByMonth.length - 1];
          if(!monthEvents || monthEvents.month !== date.getMonth()) {
            eventsByMonth.push({ month, events: [] });
            monthEvents = eventsByMonth[eventsByMonth.length - 1];
          }

          monthEvents.events.push({ name, description, category, weekDay: date.getDay(), monthDay: date.getDate(), time: formatTime(date) });
          return eventsByMonth;
        }, []);
    })
    .catch(error => {
      console.log(error);
    });
}

export default { getEvents };
