import axios from "axios";
import { API_ROUTES } from "../consts/routes";

function formatDate(date) {
  return `${("0" + (date.getDate())).slice(-2)}.${("0" + (date.getMonth() + 1)).slice(-2)}.${date.getFullYear()}, ${date.getHours()}:${("0" + date.getMinutes()).slice(-2)}`;
}

function newsResponseTransformer(news) {
  const { id, title, content, created_at, created_by: author, subject_group: sag, is_owner: isOwner, attachment } = news;
  const transformedNews = { id, title, content, date: formatDate(new Date(created_at)), author, sag, isOwner };
  if(attachment) {
    const filename = /[^\/]+$/.exec(attachment)[0];
    transformedNews.attachment = { link: attachment, filename };
  }
  return transformedNews;
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
  const { title, content, sag, attachment } = news;

  const formData = new FormData();

  formData.set("title", title);
  formData.set("content", content);
  formData.set("subject_group", sag);
  formData.set("attachment", attachment);

  const config = { headers: { 'Content-Type': 'multipart/form-data' } };

  return axios
    .post(API_ROUTES.NEWS, formData, config)
    .then(response => {
      return newsResponseTransformer(response.data)
    })
    .catch(error => {
      const { title, content, subject_group: sag } = error.response.data;
      throw { title, content, sag };
    });
}

function updateNews(news) {
  const { title, content, sag, attachment } = news;

  const formData = new FormData();

  title && formData.set("title", title);
  content && formData.set("content", content);
  sag && formData.set("subject_group", sag);
  attachment && formData.set("attachment", attachment);

  const config = { headers: { 'Content-Type': 'multipart/form-data' } };

  return axios
    .patch(API_ROUTES.NEWS_ITEM(news.id), formData, config)
    .then(response => newsResponseTransformer(response.data));
}

function deleteNews(newsId) {
  return axios
    .delete(API_ROUTES.NEWS_ITEM(newsId))
    .then(response => console.log(response));
}

export default { getNews, addNews, updateNews, deleteNews, getSags }
