import axios from 'axios';
import { localStorageService } from "../services";

export default () => {
  axios.interceptors.request.use(function (config) {
    const accessToken = localStorageService.getTokens().access;

    if(accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }

    return config;
  }, function (error) {
    return Promise.reject(error);
  });

};
