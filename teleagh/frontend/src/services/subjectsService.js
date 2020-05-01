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
      const { name, semester, general_description: generalDescription, lecturers } = response.data;

      const distinctLecturers = lecturers
        .reduce((dl, lecturerYear) => {
          const { lecturer: { id, first_name, last_name, title }, students_start_year } = lecturerYear;
          if(dl.hasOwnProperty(id)) {
            dl[id].years.push(students_start_year);
          } else {
            dl[id] = { fullName: `${title} ${first_name} ${last_name}`, years: [students_start_year] };
          }
          return dl;
        }, {});

      const processedLecturers = [];
      for(const [id, data] of Object.entries(distinctLecturers)) {
        const { fullName, years } = data;
        const yearsString = "";
        years.sort((a, b) => a - b);
        processedLecturers.push({ id, fullName, years })
      }

      return { name, semester, generalDescription, lecturers: processedLecturers };
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

function getOpinions(subjectId) {
  return Promise.resolve([
    { id: 1, content: "Ascending from the enemy abyss Ending decadent diabolic bliss Into a pit of horror it arrives", author: "Millie Petrozza" },
    { id: 2, content: "Fear becomes the flame upon the ice Ghosts under the violent sun of death Lives are cured of greed and emptiness", author: "Some random" }
  ]);
}

function addOpinion(subjectId, opinion) {
  return Promise.resolve(opinion);
}

function updateOpinion(opinion) {
  return Promise.resolve(opinion);
}

function deleteOpinion(opinionId) {
  return Promise.resolve({});
}

export default { getSubjects, getSubject, getResources, getOpinions, addOpinion, updateOpinion, deleteOpinion }
