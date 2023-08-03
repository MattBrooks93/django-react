import React, { useState } from 'react';
import { Navigate } from 'react-router-dom';

function PaymentForm({ onPaymentComplete }) {
  const [cardNumber, setCardNumber] = useState('');
  const [expirationDate, setExpirationDate] = useState('');
  const [cvc, setCvc] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    // Submit the payment data to the server
    const response = await fetch('/api/payments', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        cardNumber,
        expirationDate,
        cvc
      })
    });

    if (response.ok) {
      // Clear the form fields
      setCardNumber('');
      setExpirationDate('');
      setCvc('');
      
      // Call the callback function to indicate successful payment
      onPaymentComplete();
    } else {
      // Handle error
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Card Number:
        <input
          type="text"
          value={cardNumber}
          onChange={event => setCardNumber(event.target.value)}
          required
        />
      </label>
      <br />
      <label>
        Expiration Date:
        <input
          type="text"
          value={expirationDate}
          onChange={event => setExpirationDate(event.target.value)}
          required
        />
      </label>
      <br />
      <label>
        CVC:
        <input
          type="text"
          value={cvc}
          onChange={event => setCvc(event.target.value)}
          required
        />
      </label>
      <br />
      <button type="submit">Make Payment</button>
    </form>
  );
}

export default PaymentForm;

