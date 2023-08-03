import React, { useState } from 'react';
import { Navigate } from 'react-router-dom';

function CustomerSignUpForm({ onEmployeeSignUp }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    // Submit the sign-up data to the server
    const response = await fetch('/api/register/customer', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username,
        password,
        email
      })
    });

    if (response.ok) {
      console.log("response received")
      // Redirect the customer to the reservation form
      return <Navigate to="./CustomerLoginForm" replace={true}/>;
  } else {
      // Handle error
      console.error("An error occurred while processing the request.");
  }
  };

  return (
    <>
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
        <label>
          Email:
          <input
            type="email"
            value={email}
            onChange={event => setEmail(event.target.value)}
            required
          />
        </label>
        <br />
        <button type="submit">Sign Up</button>
      </form>
      <button onClick={onEmployeeSignUp}>Sign Up as Employee</button>
    </>
  );
}

export default CustomerSignUpForm;
