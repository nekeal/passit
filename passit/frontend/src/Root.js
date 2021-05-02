import React, {useState} from 'react';
import { Router, Switch, Route } from 'react-router-dom';
import { ThemeProvider } from 'styled-components';
import {
  ConnectionProblem,
  Dashboard,
  Events, Lecturer,
  Lecturers,
  Login,
  Memes,
  PasswordChange,
  Subject,
  Subjects
} from "./views";
import createMuiTheme from "@material-ui/core/styles/createMuiTheme";
import { MuiThemeProvider } from '@material-ui/core/styles';
import { Alert } from "@material-ui/lab";

import { createBrowserHistory } from 'history';
import { tokenInterceptor, authInterceptor } from "./interceptors";

import { APP_ROUTES } from "./consts/routes";
import {Snackbar} from "@material-ui/core";
import {SNACKBAR_TYPES} from "./consts/options";

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
  bgColor: "#F0F0F0",
  mainViolet: "#87129A"
};

function Root() {
  const [ snackbar, setSnackbar ] = useState({ open: false });

  const renderSnackBar = () => {
    const { open, severity, message } = snackbar;

    const handleClose = () => setSnackbar({ open: false });

    return (
      <Snackbar open={open} autoHideDuration={6000} onClose={handleClose} anchorOrigin={{ vertical: "top", horizontal: "center" }}>
        <Alert elevation={6} variant="filled" onClose={handleClose} severity={severity}>{ message }</Alert>
      </Snackbar>
    );
  };

  const setSnackbarState = (type, message) => setSnackbar({ open: true, severity: type, message });

  return (
    <MuiThemeProvider theme={muiTheme}>
      <ThemeProvider theme={theme}>
        <Router history={history}>
          <Switch>
            <Route exact path={APP_ROUTES.DASHBOARD}>
              <Dashboard setSnackbar={setSnackbarState}/>
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
              <PasswordChange setSnackbar={setSnackbarState}/>
            </Route>
            <Route exact path={APP_ROUTES.LECTURERS}>
              <Lecturers/>
            </Route>
            <Route exact path={APP_ROUTES.LECTURER(":id")}>
              <Lecturer/>
            </Route>
            <Route exact path={APP_ROUTES.MEMES}>
              <Memes/>
            </Route>
            <Route exact path={APP_ROUTES.CONNECTION_PROBLEM}>
              <ConnectionProblem/>
            </Route>
          </Switch>
        </Router>
        { renderSnackBar() }
      </ThemeProvider>
    </MuiThemeProvider>
  );
}

export default Root;
