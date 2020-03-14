import axios from "axios";
import { tokenInterceptor, authInterceptor } from "../helpers";


tokenInterceptor();
authInterceptor();

function getSubjects(semester) {
  return axios
    .get(`/api/subjects/?semester=${semester}`)
    .then(response => {
      return response.data;
    })
    .catch(error => console.log(error));
}

function getSubject(id) {
  return axios
    .get(`/api/subjects/${id}/`)
    .then(response => {
      return response.data;
    })
    .catch(error => console.log(error));
}

function getResources(subjectId) {
  return axios
    .get('/api/resources/')
    .then(response => {
      console.log(response.data);
      return response.data.reduce((categorizedResources, resource) => {
        const { id, name, url, category } = resource;
        categorizedResources[resource.category || "OTHER"].push({ id, name, url});
        return categorizedResources;
      }, { LECTURE: [], EXAM: [], MID_TERM_EXAM: [], OTHER: [] });
    })
    .catch(error => console.log(error));
}

export default { getSubjects, getSubject, getResources }
