import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from "framer-motion";
import './potholeModal.css';
import { useAuth0 } from '@auth0/auth0-react'

// Destructure pothole AND onClose from props
function PotholeModal({ pothole, onClose, currentOrganization }) {
    const { isAuthenticated, user } = useAuth0();
    const [selectedStatus, setSelectedStatus] = useState(null);

    const changeStatus = async (event) => {
        const newStatus = event.target.value;
        try {
            const response = await fetch(`http://127.0.0.1:5000/pothole/${pothole._id}/change_status`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ status: newStatus }) // No body needed for this request, but fetch requires it for POST
            });
            const data = await response.json();
            if (data.success) {
                setSelectedStatus(newStatus);
            } else {
                console.error("Failed to update status:", data.message);
            }
        } catch (error) {
            console.error("Error updating status:", error);
        }
    };

    useEffect(() => {
        if (pothole && (selectedStatus == null || selectedStatus == undefined)) {
            setSelectedStatus(pothole.status)
        }
    }, [pothole, selectedStatus])


    const getStatusStyle = (status) => {
        if (!status) return { color: '#757575', label: '' }; // Safety check
        switch (status.toLowerCase()) {
            case 'resolved': return { color: '#4CAF50', label: 'RESOLVED' };
            case 'in progress': return { color: '#FBFB2D', label: 'IN PROGRESS' };
            case 'open': return { color: '#C77C2C', label: 'OPEN' };
            case 'unconfirmed': return { color: '#ec1010', label: 'UNCONFIRMED' };
            default: return { color: '#757575', label: status.toUpperCase() };
        }
    };

    console.log("Current user:", user);
    console.log("Current organization in modal:", currentOrganization);

    const style = selectedStatus ? getStatusStyle(selectedStatus) : { color: '#DDDDDD', label: 'LOADING...' };

    return (
        <AnimatePresence>
            {pothole && (
                <motion.div 
                    className="modal-backdrop"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    onClick={onClose} // Closes when clicking background
                >
                    <motion.div 
                        className="modal-container"
                        initial={{ y: "100%" }}
                        animate={{ y: -260 }}
                        exit={{ y: "100%" }}
                        transition={{ type: "spring", damping: 25, stiffness: 500 }}
                        onClick={(e) => e.stopPropagation()} // Prevents closing when clicking the card itself
                    >
                        <div className="modal-content">
                            <img src={pothole.image_url} alt="pothole" />
                            <div className="modal-text">
                                <h2>({pothole.location.coordinates[0].toFixed(4)}°, {pothole.location.coordinates[1].toFixed(4)}°)</h2>
                                <div className="modal-text-strlocation">
                                    <h4>Street Name: {pothole.road_name}</h4>
                                    <h4>Street Type: {pothole.road_type.charAt(0).toUpperCase() + pothole.road_type.slice(1)}</h4>
                                </div>
                                <p>Last Updated: {pothole.detection_date}</p>
                                {
                                    (user && currentOrganization && (user.org_id == currentOrganization._id)) ?
                                    <>
                                        <label htmlFor="status">Status: </label>
                                        <select id="status" style={style} value={selectedStatus} onChange={changeStatus}>
                                            <option style={{color: 'white'}} value={"resolved"}>RESOLVED</option>
                                            <option style={{color: 'white'}} value={"in progress"}>IN PROGRESS</option>
                                            <option style={{color: 'white'}} value={"open"}>OPEN</option>
                                            <option style={{color: 'white'}} value={"unconfirmed"}>UNCONFIRMED</option>
                                        </select>
                                    </> :
                                    <p>Status: <span style={{ color: style.color, fontWeight: 'bold' }}><strong>{style.label}</strong></span></p>
                                }
                                
                                <hr />
                                <p>Width: {pothole.size.width_cm}cm</p>
                                <p>Height: {pothole.size.height_cm}cm</p>
                                <p>Confidence: {Math.round(pothole.confidence * 100)}%</p>
                                <button className="close-btn" onClick={onClose}>Close</button>
                            </div>
                        </div>
                    </motion.div>
                </motion.div>
            )}
        </AnimatePresence>
    );
}

export default PotholeModal;