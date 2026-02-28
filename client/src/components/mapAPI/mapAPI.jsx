import React from 'react';
import {APIProvider, Map, AdvancedMarker, Pin} from '@vis.gl/react-google-maps';
import './mapAPI.css';

const ROLLA_CENTER = {lat: 37.9485, lng:-91.7715};

function MapAPI({potholes}) {
    return (
        <APIProvider apiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY}>
            <Map
            style={{ width: '100%', height: '100%' }}
            defaultCenter={ROLLA_CENTER}
            defaultZoom={13}
            mapId="DEMO_MAP_ID"
            disableDefaultUI={true}
            gestureHandling={'greedy'}
            minZoom={14}
            restriction={{north: 37.980, south: 37.910, west: -91.780, east: -91.720}}
            >

            </Map>
        </APIProvider>

    );
}

export default MapAPI;