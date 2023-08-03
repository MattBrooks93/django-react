import React, { useState } from 'react';

function CustomerLoginForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    // Submit the login data to the server
    const response = await fetch('/api/login/customer', {
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
      // Redirect the customer to the reservation form
    } else {
      // Handle error
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