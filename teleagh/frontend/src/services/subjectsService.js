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
        years.sort((a, b) => a - b);
        processedLecturers.push({ id, fullName: fullName })
      }

      console.log(lecturers);

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

export default { getSubjects, getSubject, getResources }
