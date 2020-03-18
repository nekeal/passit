import axios from 'axios';
import { localStorageService, authService } from "../services";
import { APP_ROUTES, API_ROUTES } from "../consts/routes";

export default (history) => {
  axios.interceptors.response.use( (response) => {
    // Return a successful response back to the calling service
    return response;
  }, (error) => {
    // Return any error which is not due to authentication back to the calling service

    if (error.response.status === 500) {
      history.push(APP_ROUTES.CONNECTION_PROBLEM);
    }

    if (error.response.status !== 401 || error.config.url === API_ROUTES.JWT_CREATE) {
      return new Promise((resolve, reject) => {
        reject(error);
      });
    }

    const refreshToken = localStorageService.getTokens().refresh;

    // Logout user if token refresh didn't work or there is no refresh-token
    if (error.config.url === API_ROUTES.JWT_REFRESH || !refreshToken) {
      history.push(APP_ROUTES.LOGIN);
      authService.logout();

      return new Promise((resolve, reject) => {
        reject(error);
      });
    }

    // Try request again with new token
    return axios
      .post(API_ROUTES.JWT_REFRESH, { refresh: refreshToken })
      .then(response => {
        localStorageService.setTokens(response.data);
        return response.data.access;
      })
      .then((token) => {
        // New request with new token
        const config = error.config;
        config.headers['Authorization'] = `Bearer ${token}`;

        return new Promise((resolve, reject) => {
          axios.request(config).then(response => {
            resolve(response);
          }).catch((error) => {
            reject(error);
          })
        });

      })
      .catch((error) => {
        throw error;
      });
  });
}
