import React, { useState } from 'react';
import CustomerLoginForm from './components/CustomerLoginForm';
import EmployeeLoginForm from './components/EmployeeLoginForm';
import CustomerSignUpForm from './components/CustomerSignUpForm';
import EmployeeSignUpForm from './components/EmployeeSignUpForm';

function App() {
  const [showCustomerLogin, setShowCustomerLogin] = useState(false);
  const [showEmployeeLogin, setShowEmployeeLogin] = useState(false);
  const [showCustomerSignUp, setShowCustomerSignUp] = useState(false);
  const [showEmployeeSignUp, setShowEmployeeSignUp] = useState(false);

  if (showCustomerLogin) {
    return (
      <>
        <button onClick={() => setShowCustomerLogin(false)}>Back</button>
        <CustomerLoginForm />
      </>
    );
  }

  if (showEmployeeLogin) {
    return (
      <>
        <button onClick={() => setShowEmployeeLogin(false)}>Back</button>
        <EmployeeLoginForm />
      </>
    );
  }

  if (showCustomerSignUp) {
    return (
      <>
        <button onClick={() => setShowCustomerSignUp(false)}>Back</button>
        <CustomerSignUpForm onEmployeeSignUp={() => {
          setShowCustomerSignUp(false);
          setShowEmployeeSignUp(true);
        }} />
      </>
    );
  }

  if (showEmployeeSignUp) {
    return (
      <>
        <button onClick={() => setShowEmployeeSignUp(false)}>Back</button>
        <EmployeeSignUpForm />
      </>
    );
  }

  return (
    <>
      <button onClick={() => setShowCustomerLogin(true)}>
        Customer Login
      </button>
      <button onClick={() => setShowEmployeeLogin(true)}>
        Employee Login
      </button>
      <button onClick={() => setShowCustomerSignUp(true)}>
        Create Customer Account
      </button>
    </>
  );
}

export default App;
