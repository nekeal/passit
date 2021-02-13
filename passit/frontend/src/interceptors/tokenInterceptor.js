import axios from 'axios';
import { localStorageService, authService } from "../services";
import { APP_ROUTES, API_ROUTES } from "../consts/routes";

export default (history) => {
  axios.interceptors.response.use(response => {
    return response;
  }, (error) => {
    if (error.response.status === 500 || error.response.status === 502) {
      history.push(APP_ROUTES.CONNECTION_PROBLEM);
    }

    if (error.response.status !== 401 || error.config.url === API_ROUTES.JWT_CREATE) {
      return new Promise((resolve, reject) => {
        reject(error);
      });
    }

    const refreshToken = localStorageService.getTokens().refresh;

    if (error.config.url === API_ROUTES.JWT_REFRESH || !refreshToken) {
      history.push(APP_ROUTES.LOGIN);
      authService.logout();

      return new Promise((resolve, reject) => {
        reject(error);
      });
    }

    return axios
      .post(API_ROUTES.JWT_REFRESH, { refresh: refreshToken })
      .then(response => {
        localStorageService.setTokens(response.data);
        return response.data.access;
      })
      .then((token) => {
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
