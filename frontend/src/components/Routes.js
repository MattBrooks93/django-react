import React, { useState, useEffect } from 'react';
import ReservationForm from './ReservationForm';

function Routes() {
  const [routes, setRoutes] = useState([]);
  const [selectedRoute, setSelectedRoute] = useState(null);

  useEffect(() => {
    // Fetch routes data from the server
    const fetchRoutes = async () => {
      const response = await fetch('/api/routes');
      const data = await response.json();
      setRoutes(data);
    };
    fetchRoutes();
  }, []);

  if (selectedRoute) {
    return <ReservationForm route={selectedRoute} />;
  }

  return (
    <table>
      <thead>
        <tr>
          <th>Departure Location</th>
          <th>Departure Time</th>
          <th>Arrival Location</th>
          <th>Arrival Time</th>
          <th>Cost</th>
        </tr>
      </thead>
      <tbody>
        {routes.map(route => (
          <tr key={route.id} onClick={() => setSelectedRoute(route)}>
            <td>{route.departureLocation}</td>
            <td>{route.departureTime}</td>
            <td>{route.arrivalLocation}</td>
            <td>{route.arrivalTime}</td>
            <td>{route.cost}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default Routes;
