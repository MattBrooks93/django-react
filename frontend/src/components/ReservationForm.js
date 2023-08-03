import React, { useState } from 'react';
import PaymentForm from './PaymentForm';

function ReservationForm({ route }) {
    const [customerName, setCustomerName] = useState('');
    const [tripId, setTripId] = useState(route.id);
    const [numSeats, setNumSeats] = useState(1);
    const [showPaymentForm, setShowPaymentForm] = useState(false);
    const [paymentComplete, setPaymentComplete] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();

    // Submit the reservation data to the server
    const response = await fetch('/api/reservations', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        customerName,
        tripId,
        numSeats,
        paymentComplete
      })
    });

    if (response.ok) {
      // Clear the form fields
      setCustomerName('');
      setTripId('');
      setNumSeats(1);
      
      // Reset payment completion state
      setPaymentComplete(false);
    } else {
      // Handle error
    }
  };

  return (
    <>
      <form onSubmit={handleSubmit}>
        <label>
          Customer Name:
          <input
            type="text"
            value={customerName}
            onChange={event => setCustomerName(event.target.value)}
            required
          />
        </label>
        <br />
        <label>
          Trip ID:
          <input
            type="text"
            value={tripId}
            onChange={event => setTripId(event.target.value)}
            required
          />
        </label>
        <br />
        <label>
          Number of Seats:
          <input
            type="number"
            min="1"
            value={numSeats}
            onChange={event => setNumSeats(event.target.value)}
            required
          />
        </label>
        <br />
        <button type="submit">Make Reservation</button>
      </form>
      {showPaymentForm && (
        <PaymentForm onPaymentComplete={() => {
          setShowPaymentForm(false);
          setPaymentComplete(true);
        }} />
      )}
      {!paymentComplete && (
        <button onClick={() => setShowPaymentForm(true)}>
          Prepay for Reservation
        </button>
      )}
    </>
  );
}

export default ReservationForm;

