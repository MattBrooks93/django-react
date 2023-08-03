import React, { useState } from 'react';

function EmployeeSignUpForm() {
  const [employeeId, setEmployeeId] = useState('');
  const [isValidated, setIsValidated] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleValidate = async (event) => {
    event.preventDefault();

    // Validate the employee ID with the server
    const response = await fetch('/api/validate/employee', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        employeeId
      })
    });

    if (response.ok) {
      // Set isValidated state to true
      setIsValidated(true);
    } else {
      // Handle error
    }
  };

  const handleSignUp = async (event) => {
    event.preventDefault();

    // Submit the sign-up data to the server
    const response = await fetch('/api/signup/employee', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username,
        password,
        employeeId
      })
    });

    if (response.ok) {
      // Redirect the employee to the login page
    } else {
      // Handle error
    }
  };

  if (!isValidated) {
    return (
      <form onSubmit={handleValidate}>
        <label>
          Employee ID:
          <input
            type="text"
            value={employeeId}
            onChange={event => setEmployeeId(event.target.value)}
            required
          />
        </label>
        <br />
        <button type="submit">Continue</button>
      </form>
    );
  }

  return (
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
  );
}

export default EmployeeSignUpForm;
