import axios from "axios";
import { tokenInterceptor, authInterceptor } from "../helpers";


tokenInterceptor();
authInterceptor();

function getSubjects(semester) {
  return axios
    .get('/api/subjects/')
    .then(response => {
      return response.data.filter(subject => subject.semester === semester);
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
      return response.data.reduce((categorizedResources, resource) => {
        const { id, name, url } = resource;
        categorizedResources[resource.category].push({ id, name, url});
        return categorizedResources;
      }, { LECTURE: [], EXAM: [], MID_TERM_EXAM: [], OTHER: [] });
    })
    .catch(error => console.log(error));
}

export default { getSubjects, getSubject, getResources }
