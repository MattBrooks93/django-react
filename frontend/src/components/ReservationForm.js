import React, { useState } from 'react';

function ReservationForm() {
  const [customerName, setCustomerName] = useState('');
  const [tripId, setTripId] = useState('');
  const [numSeats, setNumSeats] = useState(1);

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
        numSeats
      })
    });

    if (response.ok) {
      // Clear the form fields
      setCustomerName('');
      setTripId('');
      setNumSeats(1);
    } else {
      // Handle error
    }
  };

  return (
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
  );
}

export default ReservationForm;