import axios from "axios";
import { localStorageService } from "./index";
import { API_ROUTES } from "../consts/routes";

function login(username, password) {
  return axios
    .post(API_ROUTES.JWT_CREATE, {
      username, password
    })
    .then(response => {
      localStorageService.setTokens(response.data);
    })
    .catch(error => {
      throw error.response.data;
    });
}

function logout() {
  localStorageService.removeTokens();
}

function changePassword(currentPassword, newPassword) {
  return axios
    .post(API_ROUTES.SET_PASSWORD, {
      new_password: newPassword,
      current_password: currentPassword
    })
    .catch(error => {
      const { new_password, current_password } = error.response.data;
      throw { newPassword: new_password, currentPassword: current_password };
    });
}

function profileInfo() {
  return axios
    .get(API_ROUTES.ME)
    .then(response => {
      const { first_name, last_name, profile: { memberships, field_age_groups }} = response.data;
      const fags = field_age_groups.map(fag => {
        const { id, field_of_study: { id: fieldOfStudyId, name }, students_start_year } = fag;
        const type = memberships.find(m => m.field_age_group === id).type;
        return { id, name: `${name} ${students_start_year}`, type, fieldOfStudyId };
      });
      const defaultFagId = memberships.find(m => m.is_default === true).field_age_group;
      const defaultFag = fags.find(fag => fag.id === defaultFagId);
      return { fullName: `${first_name} ${last_name}`, fags, defaultFag };
    })
    .catch(error => {
      console.log(error);
    });
}

function changeFAG(fagID) {
  return axios
    .put(API_ROUTES.SET_DEFAULT_FAG, { field_age_group: fagID })
    .then(response => {
      console.log(response.data);
      return response.data;
    })
    .catch(error => console.log(error));
}

export default { login, logout, changePassword, profileInfo, changeFAG };
