import axios from "axios";
import { API_ROUTES } from "../consts/routes";

function formatDate(date) {
  return `${("0" + (date.getDate() + 1)).slice(-2)}.${("0" + (date.getMonth() + 1)).slice(-2)}.${date.getFullYear()}, ${date.getHours()}:${("0" + date.getMinutes()).slice(-2)}`;
}

function getNews() {
  return axios
    .get(API_ROUTES.NEWS)
    .then(response => {
      return response.data.map(news => {
        const { id, title, content, created_at, created_by: author } = news;
        return { id, title, content, date: formatDate(new Date(created_at)), author };
      });
    })
    .catch(error => {
      console.log(error);
    });
}

export default { getNews }
