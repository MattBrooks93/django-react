import React, { useState } from 'react';
import axios from "axios";
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Navbar, Nav, NavDropdown } from 'react-bootstrap';
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
      <Navbar bg="light" expand="lg">
        <Navbar.Brand href="#home">Bus Reservation</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="mr-auto">
            <Nav.Link onClick={() => setShowCustomerLogin(true)}>Customer Login</Nav.Link>
            <Nav.Link onClick={() => setShowEmployeeLogin(true)}>Employee Login</Nav.Link>
            <Nav.Link onClick={() => setShowCustomerSignUp(true)}>Create Customer Account</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Navbar>

      {/* The rest of your existing code */}
      </>
  );
}


export default App;
