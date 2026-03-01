import React, { useState } from 'react';
import {APIProvider, Map, AdvancedMarker} from '@vis.gl/react-google-maps';
import './mapAPI.css';
import MapPin from '../mapPin/mapPin';
import PotholeModal from '../potholeModal/potholeModal';

const ROLLA_CENTER = {lat: 37.9485, lng:-91.7715};

function MapAPI({potholes}) {
    const [SelectedPothole, setSelectedPothole] = useState(null);
    const [modal, setModal] = useState(false);
    
    const mapStyles = [
        {
            featureType: "poi",
            elementType: "labels",
            stylers: [{ visibility: "off" }],
        },
        {
            featureType: "poi",
            elementType: "geometry",
            stylers: [{ visibility: "off" }],
        },
        {
            featureType: "transit",
            elementType: "labels.icon",
            stylers: [{ visibility: "off" }],
        },
    ];
    
    return (
            <APIProvider apiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY}>
                <Map
                style={{ width: '100%', height: '100%' }}
                defaultCenter={ROLLA_CENTER}
                defaultZoom={9}
                mapId="56e3f3ba5b24b19c7eb8f11c"
                // styles={mapStyles}
                disableDefaultUI={false}
                gestureHandling={'greedy'}
                minZoom={13.5}
                restriction={{
                    latLngBounds: {
                    north: 38.000,
                    south: 37.900,
                    west: -91.880, // Adjusted slightly west to keep Rolla centered
                    east: -91.640
                    },
                    strictBounds: false // False allows smooth bouncing; True is a hard "wall"
                }}
                >
                    {
                        potholes.map((p) => {
                            // <p>text</p>
                            return <MapPin pothole={p} onClick={() => { setSelectedPothole(p); setModal(p); }} />
                            // <Marker ref={p} position={{ lat: p['coordinates'][1], lon: p['coordinates'][0] }} />
                        })
                    }
                </Map>
                <PotholeModal pothole={SelectedPothole} onClose={() => setSelectedPothole(null)} />
            </APIProvider>
    );
}

export default MapAPI;