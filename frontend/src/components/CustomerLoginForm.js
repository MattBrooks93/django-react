import React, { useState } from 'react';
import { Navigate } from 'react-router-dom';

function CustomerLoginForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    // Submit the login data to the server
    const response = await fetch('http://localhost:8000/api/login/customer', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username,
        password,
        is_customer: true
      })
    });

    if (response.ok) {
      // Redirect the customer to the reservation form
      return <Navigate to="./Routes" />;
  } else {
      // Handle error
      console.error("An error occurred while processing the request.");
  }
  };

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

export default CustomerLoginForm;