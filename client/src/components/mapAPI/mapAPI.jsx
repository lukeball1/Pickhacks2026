import React from 'react';
import {APIProvider, Map, AdvancedMarker, Pin} from '@vis.gl/react-google-maps';
import './mapAPI.css';

const ROLLA_CENTER = {lat: 37.9485, lng:-91.7715};

function MapAPI({potholes}) {

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
            defaultZoom={12}
            mapId="56e3f3ba5b24b19c7eb8f11c"
            styles={mapStyles}
            disableDefaultUI={false}
            gestureHandling={'greedy'}
            minZoom={14}
            restriction={{
                latLngBounds: {
                north: 37.970,
                south: 37.920,
                west: -91.810, // Adjusted slightly west to keep Rolla centered
                east: -91.720
                },
                strictBounds: false // False allows smooth bouncing; True is a hard "wall"
            }}
            >

            </Map>
        </APIProvider>

    );
}

export default MapAPI;