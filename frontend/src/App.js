import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import CustomerLoginForm from './components/CustomerLoginForm';
import EmployeeLoginForm from './components/EmployeeLoginForm';
import CustomerSignUpForm from './components/CustomerSignUpForm';
import EmployeeSignUpForm from './components/EmployeeSignUpForm';
import PaymentForm from './components/PaymentForm';
import ReservationForm from './components/ReservationForm';
import styles from "./App.css";

function Navbar() {
  return (
    <div className="navbar">
      <Link className="navbar-link" to="/customer_login">Customer Login</Link>
      <Link className="navbar-link" to="/employee_login">Employee Login</Link>
      <Link className="navbar-link" to="/customer_signup">Create Customer Account</Link>
      <Link className="navbar-link" to="/employee_signup">Create Employee Account</Link>
      <Link className="navbar-link" to="/reservation">Reservation</Link>
    </div>
  );
}


function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/customer_login" element={<CustomerLoginForm />} />
        <Route path="/employee_login" element={<EmployeeLoginForm />} />
        <Route path="/customer_signup" element={<CustomerSignUpForm />} />
        <Route path="/employee_signup" element={<EmployeeSignUpForm />} />
        <Route path="/payment" element={<PaymentForm />} />
        <Route path="/reservation" element={<ReservationForm />} />
      </Routes>
    </Router>
  );
}

export default App;
