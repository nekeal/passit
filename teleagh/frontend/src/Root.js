import React from 'react';
import { Router, Switch, Route } from 'react-router-dom';
import { ThemeProvider } from 'styled-components';

import {Dashboard, Events, Lecturers, Login, Memes, PasswordChange, Subject, Subjects} from "./views";
import createMuiTheme from "@material-ui/core/styles/createMuiTheme";
import { MuiThemeProvider } from '@material-ui/core/styles';

import { createBrowserHistory } from 'history';
import { tokenInterceptor, authInterceptor } from "./helpers";

import { APP_ROUTES } from "./helpers/routes";

const history = createBrowserHistory();
tokenInterceptor(history);
authInterceptor();

const muiTheme = createMuiTheme({
  palette: {
    secondary: {
      main: '#87129A',
    },
  },
  typography: {
    fontFamily: "Roboto",
    h1: {
      fontWeight: 700,
      fontSize: '2rem'
    },
    h2: {
      fontWeight: 700,
      fontSize: '1.6rem'
    },
    h3: {
      fontWeight: 500,
      fontSize: '1.4rem'
    },
    h4: {
      fontWeight: 500,
      fontSize: '1.3rem',
      lineHeight: 2
    },
    h5: {
      fontWeight: 500,
      fontSize: '1.2rem',
      lineHeight: 1.8
    },
    h6: {
      fontWeight: 500,
      fontSize: '1.05rem',
      lineHeight: 1.6
    },
  }
});

const theme = {
  bgColor: '#F0F0F0',
};

function Root() {
  return (
    <MuiThemeProvider theme={muiTheme}>
      <ThemeProvider theme={theme}>
        <Router history={history}>
          <Switch>
            <Route exact path={APP_ROUTES.DASHBOARD}>
              <Dashboard/>
            </Route>
            <Route exact path={APP_ROUTES.LOGIN}>
              <Login/>
            </Route>
            <Route exact path={APP_ROUTES.SUBJECTS}>
              <Subjects/>
            </Route>
            <Route exact path={APP_ROUTES.SUBJECT(":id")}>
              <Subject/>
            </Route>
            <Route exact path={APP_ROUTES.EVENTS}>
              <Events/>
            </Route>
            <Route exact path={APP_ROUTES.PASSWORD_CHANGE}>
              <PasswordChange/>
            </Route>
            <Route exact path={APP_ROUTES.LECTURERS}>
              <Lecturers/>
            </Route>
            <Route exact path={APP_ROUTES.MEMES}>
              <Memes/>
            </Route>
          </Switch>
        </Router>
      </ThemeProvider>
    </MuiThemeProvider>
  );
}

export default Root;
