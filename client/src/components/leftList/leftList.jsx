import {React, useState} from 'react';
import './leftList.css';
import PotholeModal from '../potholeModal/potholeModal';
import PupilIMG from '../../assets/PUPILlogo.png';
import FilterMenu from '../filterMenu/filterMenu';
// import { useAuth0 } from '@auth0/auth0-react';

function LeftList({ allPotholes, potholes, onModalClose, onApplyFilters }){

    const [selectedPothole, setSelectedPothole] = useState(null);


    return(
        <div className="leftList">
            <div className="icon">
                <img src={PupilIMG}/>
            </div>

            <FilterMenu onApplyFilters={(roadName, streetType, status) => {
                onApplyFilters(roadName, streetType, status);
            }} />

            <div className="potholes">
                <h2>Potholes</h2>
                <ul>
                    {potholes.map((item) => {
                        // This index is now "sticky" because it always references the master list
                        const permanentIndex = allPotholes.findIndex(p => p._id === item._id) + 1;

                        return (
                            <div key={item._id} className='potholeCard'>
                                <li onClick={() => setSelectedPothole(item)}> 
                                    Pothole #{permanentIndex} - {item.road_name}
                                </li>
                            </div>
                        );
                    })}
                </ul>
                

            </div>

            {selectedPothole && (
                <PotholeModal pothole={selectedPothole} onClose={() => { setSelectedPothole(null); onModalClose(); }}/>
            )}

        </div>
    );
}

export default LeftList;