import {
  MapContainer,
  TileLayer,
  Marker,
  Popup
} from "react-leaflet";
import { useEffect, useState } from "react";
import axios from "axios";
import L from "leaflet";
import "./MapView.css"; // For popup styling

interface Location {
  location_id: number;
  latitude: number;
  longitude: number;
  risk_level: string;
  name?: string;
}

interface MapViewProps {
  onLocationSelect?: (location: Location) => void;
}

export default function MapView({ onLocationSelect }: MapViewProps) {
  const [locations, setLocations] = useState<Location[]>([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/predict_all")
      .then((res) => {
        setLocations(res.data.locations);
      })
      .catch((err) => {
        console.error("API Error:", err);
      });
  }, []);

  const getColor = (risk: string) => {
    switch (risk) {
      case "Low":
        return "#10b981";
      case "Medium":
        return "#f59e0b";
      case "High":
        return "#ef4444";
      case "Critical":
        return "#991b1b";
      default:
        return "#3b82f6";
    }
  };

  const createCustomIcon = (risk: string) => {
    const color = getColor(risk);
    return L.divIcon({
      className: 'custom-marker',
      html: `<div style="
        background-color: ${color};
        width: 32px;
        height: 32px;
        border-radius: 50%;
        border: 3px solid white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
      "></div>`,
      iconSize: [32, 32],
      iconAnchor: [16, 16],
    });
  };

  const handleMarkerClick = (loc: Location) => {
    onLocationSelect?.(loc);
  };

  return (
    <MapContainer
      center={[-37.8136, 144.9631]}
      zoom={11}
      style={{ height: "100%", width: "100%", borderRadius: "12px" }}
    >
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {locations.map((loc) => (
        <Marker
          key={loc.location_id}
          position={[loc.latitude, loc.longitude]}
          icon={createCustomIcon(loc.risk_level)}
          eventHandlers={{
            click: () => handleMarkerClick(loc)
          }}
        >
          <Popup>
            <div className="popup-content">
              <p className="popup-title">Location {loc.location_id}</p>
              <p className="popup-text">Risk: {loc.risk_level}</p>
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}