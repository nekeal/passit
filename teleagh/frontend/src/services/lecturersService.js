import axios from "axios";
import { API_ROUTES } from "../consts/routes";

function getLecturers() {
  return axios
    .get(API_ROUTES.LECTURERS)
    .then(response => {
      return response.data;
    })
    .catch(error => {
      console.log(error);
    });
}

export default { getLecturers }
