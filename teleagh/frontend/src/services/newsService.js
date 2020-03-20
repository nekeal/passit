import axios from "axios";
import { API_ROUTES } from "../consts/routes";
import authService from "./authService";

function formatDate(date) {
  return `${("0" + (date.getDate())).slice(-2)}.${("0" + (date.getMonth() + 1)).slice(-2)}.${date.getFullYear()}, ${date.getHours()}:${("0" + date.getMinutes()).slice(-2)}`;
}

function newsResponseTransformer(news) {
  const { id, title, content, created_at, created_by: author, subject_group: sag, is_owner: isOwner } = news;
  return { id, title, content, date: formatDate(new Date(created_at)), author, sag, isOwner };
}

function getNews(fagId) {
  return axios
    .get(API_ROUTES.NEWS_FAG(fagId))
    .then(response => {
      return response.data.map(newsResponseTransformer);
    })
}

function getSags(fag) {
  return axios
    .get(API_ROUTES.SAGS(fag))
    .then(response => response.data.map(sag => {
      const { id, subject_name } = sag;
      return { id, subjectName: subject_name };
    }));
}

function addNews(news) {
  const { title, content, sag } = news;
  return axios
    .post(API_ROUTES.NEWS, { title, content, subject_group: sag })
    .then(response => newsResponseTransformer(response.data));
}

function updateNews(news) {
  return axios
    .patch(API_ROUTES.NEWS_ITEM(news.id), news)
    .then(response => newsResponseTransformer(response.data));
}

function deleteNews(newsId) {
  return axios
    .delete(API_ROUTES.NEWS_ITEM(newsId))
    .then(response => console.log(response));
}

export default { getNews, addNews, updateNews, deleteNews, getSags }
