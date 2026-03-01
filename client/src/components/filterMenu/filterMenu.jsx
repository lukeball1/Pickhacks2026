import './filterMenu.css';
import { useState } from 'react';

function FilterMenu({onApplyFilters}) {
    const [roadName, setRoadName] = useState("");
    const [streetType, setStreetType] = useState("");
    const [status, setStatus] = useState(""); 

    return <form className="filterMenu">
      <h3>Filter Potholes</h3>

      <label htmlFor="roadName">Road Name:</label>
      <input type="text" id="roadName" value={roadName} onChange={(e) => setRoadName(e.target.value)} />
      <br />

      <label htmlFor="streetType">Street Type:</label>
      <select id="streetType" value={streetType} onChange={(e) => setStreetType(e.target.value)}>
        <option value="">All</option>
        <option value="primary">Primary</option>
        <option value="secondary">Secondary</option>
        <option value="tertiary">Tertiary</option>
        <option value="motorway">Motorway</option>
        <option value="residential">Residential</option>
        <option value="unclassified">Unclassified</option>
      </select>
      <br />

      <label htmlFor="status">Status:</label>
      <select id="status" value={status} onChange={(e) => setStatus(e.target.value)}>
        <option value="">All</option>
        <option value="open">Open</option>
        <option value="in progress">In Progress</option>
        <option value="resolved">Resolved</option>
        <option value="unconfirmed">Unconfirmed</option>
      </select>
      <br />

      <button type="button" onClick={() => onApplyFilters(roadName, streetType, status)}>Apply Filters</button>
    </form>
}

export default FilterMenu;