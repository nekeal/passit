import React, {useState} from 'react';
import { authService } from "../../services";

function Dashboard() {
  const [ username, setUsername ] = useState('');
  const [ password, setPassword ] = useState('');
  const [ currentPassword, setCurrentPassword ] = useState('');
  const [ newPassword, setNewPassword ] = useState('');
  const [ currentPasswordErrors, setCurrentPasswordErrors ] = useState([]);
  const [ newPasswordErrors, setNewPasswordErrors ] = useState([]);
  const [ message, setMessage ] = useState('');

  return (
    <div className="Dashboard">
      Dashboard
      <div>
        { message }
      </div>
      <div>
        Login
        <div>
          Username
          <input type="text" value={username} onChange={event => setUsername(event.target.value)}/>
        </div>
        <div>
          Password
          <input type="password" value={password} onChange={event => setPassword(event.target.value)}/>
        </div>
        <button onClick={() => {
          authService.login(username, password);
        }}>Login</button>
      </div>
      <div>
        Change password
        <div>
          Current password
          <input type="text" value={currentPassword} onChange={event => setCurrentPassword(event.target.value)}/>
          { currentPasswordErrors.map(error => <div>{error}</div>) }
        </div>
        <div>
          New password
          <input type="password" value={newPassword} onChange={event => setNewPassword(event.target.value)}/>
          { newPasswordErrors.map(error => <div>{error}</div>) }
        </div>
        <button onClick={() => {
          authService
            .changePassword(currentPassword, newPassword)
            .then(() => {
              setMessage('Password successfully changed');
            })
            .catch(error => {
              if(error.currentPassword) {
                setCurrentPasswordErrors(error.currentPassword);
              }
              if(error.newPassword) {
                setNewPasswordErrors(error.newPassword);
              }
            });
        }}>Set password</button>

      </div>
    </div>
  );
}

export default Dashboard;
