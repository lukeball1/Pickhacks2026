import { useState, useEffect } from 'react'
import LeftList from "./components/leftList/leftList";
import MapAPI from "./components/mapAPI/mapAPI"
import './App.css'

function App() {
  const [potholes, setPotholes] = useState(["1", "2"]);

  // useEffect(() => {
  //   async function loadPotholes(){
  //     try{
  //       const result = await fetch ("localhost:5000/potholes");
  //       const data = await result.json();

  //       if (data.success){
  //         setPotholes(data.data);
  //       }

  //     } catch (err) {
  //       console.error(err);
  //     }
  //   }
  // }, []);

  return(
    <div className='app'>
      <div className="leftSide">
        <LeftList potholes={potholes}/>
      </div>
      <div className="rightSide">
        <MapAPI potholes={potholes}/>
        <p>asladfj</p>
      </div>
    </div>
  )

}

export default App
