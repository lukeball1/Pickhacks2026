import { React, useState, useEffect } from 'react';
import './leftList.css';
import PotholeModal from '../potholeModal/potholeModal';
import PupilIMG from '../../assets/PUPILlogo.png';
import FilterMenu from '../filterMenu/filterMenu';
// import { useAuth0 } from '@auth0/auth0-react';

function LeftList({ allPotholes, potholes, onModalClose, onApplyFilters, onOrganizationChange }){

    const [selectedPothole, setSelectedPothole] = useState(null);
    const [selectedOrg, setSelectedOrg] = useState(null);
    const [orgs, setOrgs] = useState([]);

    const fetchOrgs = async () => {
        try {
            const result = await fetch("http://127.0.0.1:5000/organizations");
            // console.log(await result.text());
            const data = await result.json();
            if (data.success) {
                setOrgs(data.organizations);
            }
        }
        catch (error) {
            console.error("Error fetching organizations:", error);
        }
    };

    useEffect(() => {
        if (orgs.length === 0) {
            fetchOrgs();
        }
    }, [orgs]);

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

            <select value={selectedOrg} onChange={(e) => { setSelectedOrg(e.target.value); onOrganizationChange(e.target.value); } }>
                {
                    orgs.map((org, index) => (
                        <option key={index} value={org.name}>{org.name}</option>
                    ))
                }
            </select>

            {selectedPothole && (
                <PotholeModal pothole={selectedPothole} currentOrganization={selectedOrg} onClose={() => { setSelectedPothole(null); onModalClose(); }}/>
            )}

        </div>
    );
}

export default LeftList;