import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from "framer-motion";
import './potholeModal.css';
import { useAuth0 } from '@auth0/auth0-react'

// Destructure pothole AND onClose from props
function PotholeModal({ pothole, onClose }){
    const { isAuthenticated } = useAuth0();
    const [selectedStatus, setSelectedStatus] = useState();

    useEffect(() => {
        if (pothole) {
            setSelectedStatus(pothole.status)
        }
    }, [selectedStatus])


    const getStatusStyle = (status) => {
        if (!status) return { color: '#757575', label: '' }; // Safety check
        switch (status.toLowerCase()) {
            case 'resolved': return { color: '#4CAF50', label: 'RESOLVED' };
            case 'in progress': return { color: '#FBC02D', label: 'IN PROGRESS' };
            case 'open': return { color: '#FF9800', label: 'OPEN' };
            case 'unconfirmed': return { color: '#ec1010', label: 'UNCONFIRMED' };
            default: return { color: '#757575', label: status.toUpperCase() };
        }
    };

    const style = pothole ? getStatusStyle(pothole.status) : null;

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
                        animate={{ y: -175 }}
                        exit={{ y: "100%" }}
                        transition={{ type: "spring", damping: 25, stiffness: 500 }}
                        onClick={(e) => e.stopPropagation()} // Prevents closing when clicking the card itself
                    >
                        <div className="modal-content">
                            <img src={pothole.image_url} alt="pothole" />
                            <div className="modal-text">
                                <h2>({pothole.location.coordinates[1].toFixed(4)}°, {pothole.location.coordinates[0].toFixed(4)}°)</h2>
                                <p>Status: {
                                    isAuthenticated ?
                                    <select value={selectedStatus}>
                                        <option value={"resolved"}>RESOLVED</option>
                                        <option value={"in progress"}>IN PROGRESS</option>
                                        <option value={"open"}>OPEN</option>
                                        <option value={"unconfirmed"}>UNCONFIRMED</option>
                                    </select> :
                                    <strong>{pothole.status.toUpperCase()}</strong>
                                    }
                                </p>
                                <p>Status: <span style={{ color: style.color, fontWeight: 'bold' }}><strong>{style.label}</strong></span></p>
                                <hr />
                                <p>Width: {pothole.size.width_cm}cm</p>
                                <p>Depth: {pothole.size.depth_cm}cm</p>
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