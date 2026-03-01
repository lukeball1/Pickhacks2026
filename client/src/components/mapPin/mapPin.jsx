import {AdvancedMarker, Marker, Pin, useAdvancedMarkerRef, useMarkerRef} from '@vis.gl/react-google-maps';
import { useEffect, useState } from 'react';

function MapPin({pothole, onClick}) {
  const [markerRef, marker] = useAdvancedMarkerRef()
  const [backgroundColor, setBackgroundColor] = useState('hsl(0 100% 50%)')

  useEffect(() => {
    // const risk_score = (pothole['size']['width_cm'] * pothole['size']['depth_cm']) ** (1/2)
    const risk_score = Math.sqrt(pothole['size']['width_cm'] * pothole['size']['depth_cm'])
    // console.log(pothole['size']['width_cm'], pothole['size']['depth_cm'])

    // console.log("risk: ", risk_score)

    const hue = Math.round(180 - (risk_score * 12))

    // console.log(hue)

    const color = 'hsl(' + ((hue > 0) ? hue : 0) + ' 100% 50%)'
    // console.log(color)
    setBackgroundColor(color)
    
    if (!marker) { 
      return;
    }

  }, [marker, backgroundColor])

  return (
    <AdvancedMarker ref={markerRef} position={{ lat: pothole['location']['coordinates'][1], lng: pothole['location']['coordinates'][0] }} onClick={() => {onClick()} }>
      <Pin background={backgroundColor} glyphColor={'#000'} borderColor={'#000'} />
    </AdvancedMarker>
  )
}

export default MapPin;