import {AdvancedMarker, Marker, Pin, useAdvancedMarkerRef, useMarkerRef} from '@vis.gl/react-google-maps';
import { useEffect } from 'react';

function MapPin({pothole, onClick}) {
  const [markerRef, marker] = useAdvancedMarkerRef()

  useEffect(() => {
    if (!marker) { 
      return;
    }

  }, [marker])

  return (
    <AdvancedMarker ref={markerRef} position={{ lat: pothole['location']['coordinates'][1], lng: pothole['location']['coordinates'][0] }} onClick={() => {onClick()} }>
      <Pin background={'#FF0000'} glyphColor={'#000'} borderColor={'#000'} />
    </AdvancedMarker>
  )
}

export default MapPin;