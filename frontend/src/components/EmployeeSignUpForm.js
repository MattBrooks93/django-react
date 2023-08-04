import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function EmployeeSignUpForm() {

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();


  const handleSignUp = async (event) => {
    event.preventDefault();

    // Submit the sign-up data to the server
    const response = await fetch('/api/register/employee', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username,
        password
      })
    });

    if (response.ok) {
      navigate('/employee_login');
    } else {
      // Handle error
    }
  };

  return (
    <>
    <form onSubmit={handleSignUp}>
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
      <button type="submit">Sign Up</button>
    </form>
    </>
  );
}

export default EmployeeSignUpForm;
