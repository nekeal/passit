import axios from "axios";
import { API_ROUTES } from "../consts/routes";

function getSubjects(semester, fieldOfStudyId) {
  return axios
    .get(API_ROUTES.SUBJECTS(semester, fieldOfStudyId))
    .then(response => {
      return response.data;
    })
    .catch(error => console.log(error));
}

function getSubject(id) {
  return axios
    .get(API_ROUTES.SUBJECT(id))
    .then(response => {
      return response.data;
    })
    .catch(error => console.log(error));
}

function getResources(subjectId, category) {
  return axios
    .get(API_ROUTES.RESOURCES(subjectId, category))
    .then(response => {
      return response.data.map(resource => {
        const { id, name, url } = resource;

        let type;
        if(url.match(/\.pdf/)) type = "pdf";
        else if(url.match(/\.png/)) type = "photo";
        else type = "link";

        return { id, name, url, type };
      });
    })
    .catch(error => console.log(error));
}

export default { getSubjects, getSubject, getResources }
