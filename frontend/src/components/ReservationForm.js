import React, { useState } from "react";
import PaymentForm from "./PaymentForm";
import { useNavigate } from "react-router-dom";

function ReservationForm({ route }) {
  const [customerName, setCustomerName] = useState("");
  const [tripId, setTripId] = useState(route?.id || "");
  const [numSeats, setNumSeats] = useState(1);
  const [showPaymentForm, setShowPaymentForm] = useState(false);
  const [paymentComplete, setPaymentComplete] = useState(false);
  const [selectedTimeSlot, setSelectedTimeSlot] = useState("");

  const navigate = useNavigate();

  const checkSeatAvailability = async (day, timeSlot) => {
      if (true) {
        setShowPaymentForm(true);
      }
  };

  return (
    <>
      {/* Schedule table */}
      <table>
        <thead>
          <tr>
            <th>Day</th>
            <th>1:00</th>
            <th>2:00</th>
            <th>3:00</th>
            <th>4:00</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Sunday</td>
            <td>
              <button onClick={() => checkSeatAvailability("Sunday", "11AM")}>
                Check Availability
              </button>
            </td>
            <td>
              <button onClick={() => checkSeatAvailability("Sunday", "2PM")}>
                Check Availability
              </button>
            </td>
            <td>
              <button onClick={() => checkSeatAvailability("Sunday", "5PM")}>
                Check Availability
              </button>
            </td>
            <td>
              <button onClick={() => checkSeatAvailability("Sunday", "9PM")}>
                Check Availability
              </button>
            </td>
          </tr>
          <tr>
            <td>Monday</td>
            <td>
              <button onClick={() => checkSeatAvailability("Monday", "11AM")}>
                Check Availability
              </button>
            </td>
            <td>
              <button onClick={() => checkSeatAvailability("Monday", "2PM")}>
                Check Availability
              </button>
            </td>
            <td>
              <button onClick={() => checkSeatAvailability("Monday", "5PM")}>
                Check Availability
              </button>
            </td>
            <td>
              <button onClick={() => checkSeatAvailability("Monday", "9PM")}>
                Check Availability
              </button>
            </td>
          </tr>
          <tr>
            <td>Tuesday</td>
            <td>
              <button onClick={() => checkSeatAvailability("Tuesday", "11AM")}>
                Check Availability
              </button>
            </td>
            <td>
              <button onClick={() => checkSeatAvailability("Tuesday", "2PM")}>
                Check Availability
              </button>
            </td>
            <td>
              <button onClick={() => checkSeatAvailability("Tuesday", "5PM")}>
                Check Availability
              </button>
            </td>
            <td>
              <button onClick={() => checkSeatAvailability("Tuesday", "9PM")}>
                Check Availability
              </button>
            </td>
            </tr>
            <tr>
            <td>Wednesday</td>
            <td>
              <button onClick={() => checkSeatAvailability("Tuesday", "11AM")}>
                Check Availability
              </button>
            </td>
            <td>
              <button onClick={() => checkSeatAvailability("Tuesday", "2PM")}>
                Check Availability
              </button>
            </td>
            <td>
              <button onClick={() => checkSeatAvailability("Tuesday", "5PM")}>
                Check Availability
              </button>
            </td>
            <td>
              <button onClick={() => checkSeatAvailability("Tuesday", "9PM")}>
                Check Availability
              </button>
            </td>
            </tr>
            <tr>
            <td>Thursday</td>
            <td>
              <button onClick={() => checkSeatAvailability("Tuesday", "11AM")}>
                Check Availability
              </button>
            </td>
            <td>
              <button onClick={() => checkSeatAvailability("Tuesday", "2PM")}>
                Check Availability
              </button>
            </td>
            <td>
              <button onClick={() => checkSeatAvailability("Tuesday", "5PM")}>
                Check Availability
              </button>
            </td>
            <td>
              <button onClick={() => checkSeatAvailability("Tuesday", "9PM")}>
                Check Availability
              </button>
            </td>
            </tr>
            <tr>
            <td>Friday</td>
            <td>
              <button onClick={() => checkSeatAvailability("Tuesday", "11AM")}>
                Check Availability
              </button>
            </td>
            <td>
              <button onClick={() => checkSeatAvailability("Tuesday", "2PM")}>
                Check Availability
              </button>
            </td>
            <td>
              <button onClick={() => checkSeatAvailability("Tuesday", "5PM")}>
                Check Availability
              </button>
            </td>
            <td>
              <button onClick={() => checkSeatAvailability("Tuesday", "9PM")}>
                Check Availability
              </button>
            </td>
            </tr>
            <tr>
            <td>Saturday</td>
            <td>
              <button onClick={() => checkSeatAvailability("Tuesday", "11AM")}>
                Check Availability
              </button>
            </td>
            <td>
              <button onClick={() => checkSeatAvailability("Tuesday", "2PM")}>
                Check Availability
              </button>
            </td>
            <td>
              <button onClick={() => checkSeatAvailability("Tuesday", "5PM")}>
                Check Availability
              </button>
            </td>
            <td>
              <button onClick={() => checkSeatAvailability("Tuesday", "9PM")}>
                Check Availability
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      {showPaymentForm && (
        <PaymentForm
          onPaymentComplete={() => {
            setShowPaymentForm(false);
            setPaymentComplete(true);
          }}
        />
      )}
    </>
  );
}

export default ReservationForm;
