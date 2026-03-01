import { useState, useEffect } from 'react';
import LeftList from "./components/leftList/leftList";
import MapAPI from "./components/mapAPI/mapAPI";
import './App.css';
import { useAuth0 } from '@auth0/auth0-react'


function App() {
  const [potholes, setPotholes] = useState([]);

  const [filteredPotholes, setFilteredPotholes] = useState([]);
  const [region, setRegion] = useState(null);
  const [selectedOrg, setSelectedOrg] = useState(null);
  
  const { loginWithRedirect, isAuthenticated, isLoading, logout, error, user } = useAuth0();

  const [allPotholes, setAllPotholes] = useState([]);

  const loadPotholes = async (org) => {
    console.log("pothole function called");
    if (!org) {
      return;
    }
    try {
      const URL = `http://127.0.0.1:5000/potholes/${org._id}`;
      const result = await fetch (URL);
      const data = await result.json();
      
      if (data.success){
        setPotholes(data.potholes);
        setAllPotholes(data.potholes);
        console.log("successfully loaded pothole data");
      }
      
    } catch (err) {
      console.error(err);
      console.log("error in loading potholes");
    }
  }

  const selectOrganization = async (org_name) => {
    const result = await fetch(`http://127.0.0.1:5000/organizations/${org_name}`);
    const data = await result.json();
    if (data.success) {
      const org = data.organization;
      setRegion(org.region);
      setSelectedOrg(org);
      // applyRegionFilter(org.region);
      loadPotholes(org);
      console.log("Selected organization region:", org);
    }
  }

  const applyFilters = (roadName, streetType, status) => {
    const filtered = potholes.filter(pothole => {
      const matchesRoadName = roadName ? pothole.road_name.toLowerCase().includes(roadName.toLowerCase()) : true;
      const matchesStreetType = streetType ? pothole.road_type.toLowerCase() === streetType.toLowerCase() : true;
      const matchesStatus = status ? pothole.status.toLowerCase() === status.toLowerCase() : true;
      return matchesRoadName && matchesStreetType && matchesStatus;
    });
    setFilteredPotholes(filtered);
  }

  const applyRegionFilter = (region) => {
    const filtered = potholes.filter(pothole => {
      return (pothole.location.coordinates[0] >= region.min_lat && pothole.location.coordinates[0] <= region.max_lat) &&
             (pothole.location.coordinates[1] >= region.min_lng && pothole.location.coordinates[1] <= region.max_lng);
    });
    setFilteredPotholes(filtered);
    setRegion(region);
  }
  
  useEffect(() => {
    if (potholes.length == 0) {
      loadPotholes();
    }
    if (selectedOrg === null) { 
      
    }
  }, [potholes, selectedOrg]);
  
  if (isLoading) {
    return (
      <h1>Loading</h1>
    )
  }

  return(
    <div className='app'>
      <div className="leftSide">
        <LeftList allPotholes = {allPotholes} potholes={(filteredPotholes.length > 0 ? filteredPotholes : potholes)} onModalClose={loadPotholes} onApplyFilters={applyFilters} onOrganizationChange={selectOrganization} currentOrganization={selectedOrg}/>
        {
          isAuthenticated ?
          (<button onClick={logout} >LOG OUT</button>) :
          (<button onClick={loginWithRedirect} >LOG IN</button>)
        }
      </div>
      <div className="rightSide">
        <MapAPI potholes={(filteredPotholes.length > 0 ? filteredPotholes : potholes)} onModalClose={loadPotholes} region={region} currentOrganization={selectedOrg}/>
      </div>
    </div>
  )

}

export default App;
