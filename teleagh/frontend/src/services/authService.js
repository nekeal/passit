import axios from "axios";
import { localStorageService } from "./index";

function login(username, password) {
  return axios
    .post('/api/auth/jwt/create/', {
      username, password
    })
    .then(response => {
      localStorageService.setTokens(response.data);
    })
    .catch(error => {
      console.log(error.response.data);
      throw error.response.data.detail;
    });
}

function logout() {
  localStorageService.removeTokens();
}

export default { login, logout };
