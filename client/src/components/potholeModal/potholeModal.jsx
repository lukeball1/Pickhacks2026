import React from 'react';
import { motion, AnimatePresence } from "framer-motion";
import './potholeModal.css';

// Destructure pothole AND onClose from props
function PotholeModal({ pothole, onClose }){
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
                                <p>Status: <strong>{pothole.status.toUpperCase()}</strong></p>
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