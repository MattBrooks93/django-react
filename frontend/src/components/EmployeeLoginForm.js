import React, { useState } from 'react';
import BusSchedule from './BusSchedule';
import { useNavigate } from 'react-router-dom';


function EmployeeLoginForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();


  const handleSubmit = async (event) => {
    event.preventDefault();

    // Submit the login data to the server
    const response = await fetch('http://localhost:8000/api/login/employee', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username,
        password,
        is_customer: false
      })
    });

    if (response.ok) {
      // Set isLoggedIn state to true
      setIsLoggedIn(true);
      navigate('/employee_login');
    } else {
      // Handle error
    }
  };

  if (isLoggedIn) {
    return <BusSchedule />;
  }

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Username:
        <input
          type="text"
          value={username}
          onChange={event => setUsername(event.target.value)}
          required
        />
      </label>
      <br />
      <label>
        Password:
        <input
          type="password"
          value={password}
          onChange={event => setPassword(event.target.value)}
          required
        />
      </label>
      <br />
      <button type="submit">Log In</button>
    </form>
  );
}

export default EmployeeLoginForm;
