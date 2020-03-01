import axios from "axios";
import { localStorageService } from "./index";
import { tokenInterceptor, authInterceptor } from "../helpers";

authInterceptor();
tokenInterceptor();

function login(username, password) {
  return axios
    .post('/api/auth/jwt/create/', {
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
    .post('/api/auth/users/set_password/', {
      new_password: newPassword,
      current_password: currentPassword
    })
    .catch(error => {
      const { new_password, current_password } = error.response.data;
      throw { newPassword: new_password, currentPassword: current_password };
    });

}

export default { login, logout, changePassword };
