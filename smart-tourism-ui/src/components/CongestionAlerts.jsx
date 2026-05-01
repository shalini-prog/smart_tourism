import { AlertTriangle, Navigation } from "lucide-react";
import "./CongestionAlerts.css";

export default function CongestionAlerts({ locations, onLocationClick }) {
  const getStatusLabel = (risk) => {
    switch (risk) {
      case "Critical":
      case "High":
        return { text: "CROWDED", className: "status-red" };
      case "Medium":
        return { text: "MODERATE", className: "status-orange" };
      case "Low":
        return { text: "CALM", className: "status-green" };
      default:
        return { text: "STEADY", className: "status-blue" };
    }
  };

  const getRiskBadge = (risk) => {
    if (risk === "High" || risk === "Critical") {
      return <span className="risk-badge">RISK: HIGH</span>;
    }
    return null;
  };

  const sortedLocations = [...locations].sort((a, b) => {
    const order = { "Critical": 0, "High": 1, "Medium": 2, "Low": 3 };
    return (order[a.risk_level] || 4) - (order[b.risk_level] || 4);
  });

  return (
    <div className="congestion-container">
      <h2 className="congestion-title">Tourist Congestion Alerts</h2>

      <div className="locations-list">
        {sortedLocations.map((loc, index) => {
          const status = getStatusLabel(loc.risk_level);
          const riskBadge = getRiskBadge(loc.risk_level);

          return (
            <div
              key={loc.location_id}
              className="location-card"
              onClick={() => onLocationClick && onLocationClick(loc)}
            >
              <div className="location-content">
                <div className="location-image">
                  <img
                    src={`https://images.pexels.com/photos/${3290068 + index}/pexels-photo-${3290068 + index}.jpeg?auto=compress&cs=tinysrgb&w=200`}
                    alt={`Location ${loc.location_id}`}
                  />
                </div>

                <div className="location-info">
                  <div className="location-header">
                    <h3>{loc.name || `Heritage Site ${loc.location_id}`}</h3>
                    <span className={`status-label ${status.className}`}>{status.text}</span>
                  </div>

                  <p className="location-visitors">
                    Tamil Nadu, {loc.visitors || Math.floor(Math.random() * 500 + 100)} visitors
                  </p>

                  {(loc.risk_level === "High" || loc.risk_level === "Critical") && (
                    <div className="congestion-alert">
                      <AlertTriangle className="alert-icon" />
                      <p>Expected congestion today, 8AM - 2PM.</p>
                    </div>
                  )}

                  <div className="location-footer">
                    {riskBadge && <div className="risk-container">{riskBadge}</div>}
                    <button className="directions-btn">
                      <Navigation className="nav-icon" />
                      Get Directions
                    </button>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}