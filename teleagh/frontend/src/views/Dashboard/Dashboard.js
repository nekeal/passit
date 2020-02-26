import React from 'react';
import { authService } from "../../services";

function Dashboard() {

  authService.login('user', 'user1');

  return (
    <div className="Dashboard">
      Dashboard
    </div>
  );
}

export default Dashboard;
