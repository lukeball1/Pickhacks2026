import { useState, useEffect } from 'react';
import LeftList from "./components/leftList/leftList";
import MapAPI from "./components/mapAPI/mapAPI";
import './App.css';
import { useAuth0 } from '@auth0/auth0-react'


function App() {
  const [potholes, setPotholes] = useState([]);
  
  const { loginWithRedirect, isAuthenticated, isLoading, logout, error } = useAuth0();

  const loadPotholes = async () => {
    console.log("pothole function called");
    try{
      const result = await fetch ("http://127.0.0.1:5000/");
      const data = await result.json();
      
      if (data.success){
        setPotholes(data.potholes);
        console.log("successfully loaded pothole data");
      }
      
    } catch (err) {
      console.error(err);
      console.log("error in loading potholes");
    }
  }
  
  useEffect(() => {
    if (potholes.length == 0) {
      loadPotholes();
    }
  }, [potholes]);
  
  if (isLoading) {
    return (
      <h1>Loading</h1>
    )
  }

  return(
    <div className='app'>
      <div className="leftSide">
        <LeftList potholes={potholes} onModalClose={loadPotholes}/>
        {
          isAuthenticated ?
          (<button onClick={logout} >LOG OUT</button>) :
          (<button onClick={loginWithRedirect} >LOG IN</button>)
        }
      </div>
      <div className="rightSide">
        <MapAPI potholes={potholes} onModalClose={loadPotholes}/>
      </div>
    </div>
  )

}

export default App;
