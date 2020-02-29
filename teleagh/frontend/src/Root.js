import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

import { Dashboard } from "./views";

function Root() {
  return (
    <div className="Root">
      <Router>
        <Switch>
          <Route exact path='/'>
            <Dashboard/>
          </Route>
        </Switch>
      </Router>
    </div>
  );
}

export default Root;
