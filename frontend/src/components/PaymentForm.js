import React, { useState } from 'react';

function PaymentForm() {
  const [cardNumber, setCardNumber] = useState('');
  const [expirationDate, setExpirationDate] = useState('');
  const [cvc, setCvc] = useState('');
  const [paymentCompleted, setPaymentCompleted] = useState(false);

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

    if (true) {
      // Clear the form fields
      setCardNumber('');
      setExpirationDate('');
      setCvc('');

      // Set payment completed
      setPaymentCompleted(true);
    } else {
      // Handle error
    }
  };

  if(paymentCompleted) {
    return <div>Payment Successful! Details of the trip have been emailed!</div>
  }

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <text>Seats are available for the following trips!</text>
      </div>
      <div>
        <select>
          <option value="" disabled selected>
            Departing City
          </option>
          <option value="Atlanta">Atlanta</option>
          <option value="Dahlonega">Dahlonega</option>
          <option value="Athens">Athens</option>
        </select>
        <br />
        <select>
          <option value="" disabled selected>
            Arrival City
          </option>
          <option value="Marrieta">Marrieta</option>
          <option value="Cumming">Cumming</option>
          <option value="Roswell">Roswell</option>
        </select>
      </div>
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
