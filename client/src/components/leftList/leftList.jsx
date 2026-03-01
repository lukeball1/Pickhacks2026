import {React, useState} from 'react';
import './leftList.css';
import PotholeModal from '../potholeModal/potholeModal';
// import { useAuth0 } from '@auth0/auth0-react';

function LeftList({ potholes }){

    const [selectedPothole, setSelectedPothole] = useState(null);


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
                            <li
                            style={{ cursor: "pointer"}}
                            onClick={() => 
                                setSelectedPothole(item)
                            }
                            > Pothole #{index + 1}</li>
                        </div>
                    ))}
                </ul>
                

            </div>

            <PotholeModal pothole={selectedPothole} onClose={() => setSelectedPothole(null)}/>

        </div>
    );
}

export default LeftList;