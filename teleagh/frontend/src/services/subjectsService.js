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

function getResources(subjectId) {
  return axios
    .get(API_ROUTES.RESOURCES(subjectId))
    .then(response => {
      return response.data.reduce((categorizedResources, resource) => {
        const { id, name, url, category } = resource;

        let type;
        if(url.match(/\.pdf/)) type = "pdf";
        else if(url.match(/\.png/)) type = "photo";
        else type = "link";

        categorizedResources[category || "OTHER"].push({ id, name, url, type });
        return categorizedResources;
      }, { LECTURE: [], EXAM: [], MID_TERM_EXAM: [], OTHER: [] });
    })
    .catch(error => console.log(error));
}

export default { getSubjects, getSubject, getResources }
