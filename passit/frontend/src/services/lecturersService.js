import axios from "axios";
import { API_ROUTES } from "../consts/routes";

function lecturersResponseTransformer(lecturer) {
  const { id, first_name, last_name, title, contact, consultations } = lecturer;
  return { id, fullName: `${first_name} ${last_name}` };
}

function getLecturers() {
  return axios
    .get(API_ROUTES.LECTURERS)
    .then(response => {
      return response.data.map(lecturersResponseTransformer);
    })
    .catch(error => {
      console.log(error);
    });
}

export default { getLecturers }
