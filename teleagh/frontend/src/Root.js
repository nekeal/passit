import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import { ThemeProvider } from 'styled-components';

import {Dashboard, Login, Subject, Subjects} from "./views";
import createMuiTheme from "@material-ui/core/styles/createMuiTheme";
import { MuiThemeProvider } from '@material-ui/core/styles';

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
        <Router>
          <Switch>
            <Route exact path='/'>
              <Dashboard/>
            </Route>
            <Route exact path='/login'>
              <Login/>
            </Route>
            <Route exact path='/subjects'>
              <Subjects/>
            </Route>
            <Route exact path='/subjects/:id'>
              <Subject/>
            </Route>
          </Switch>
        </Router>
      </ThemeProvider>
    </MuiThemeProvider>
  );
}

export default Root;
