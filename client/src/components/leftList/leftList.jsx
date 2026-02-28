import React from 'react';
import './leftList.css';
// import { useAuth0 } from '@auth0/auth0-react';

function LeftList({ potholes }){

    

    return(
        <div className="leftList">
            <div className="icon">
                <h1>PUPIL</h1>
            </div>

            <div className="potholes">
                <h2>Potholes</h2>
                <ul>
                    {potholes.map((item, index) => (
                        <div
                        key={index}
                        className='potholeCard'
                        >
                            <li> Pothole #{item.id}</li>
                        </div>
                    ))}
                </ul>
                

            </div>
        </div>
    );
}

export default LeftList;