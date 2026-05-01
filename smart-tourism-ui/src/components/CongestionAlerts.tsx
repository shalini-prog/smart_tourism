import { AlertTriangle, Navigation } from "lucide-react";
import "./CongestionAlerts.css";

export default function CongestionAlerts({ locations, onLocationClick }) {
  const getStatus = (risk) => {
    switch (risk) {
      case "Critical":
      case "High":   return { text: "CROWDED",  cls: "badge-red" };
      case "Medium": return { text: "MODERATE", cls: "badge-orange" };
      case "Low":    return { text: "CALM",     cls: "badge-green" };
      default:       return { text: "STEADY",   cls: "badge-blue" };
    }
  };

  const sorted = [...locations].sort((a, b) => {
    const o = { Critical: 0, High: 1, Medium: 2, Low: 3 };
    return (o[a.risk_level] ?? 4) - (o[b.risk_level] ?? 4);
  });

  return (
    <div className="ca-wrap">
      <h2 className="ca-heading">Tourist Congestion Alerts</h2>

      <div className="ca-list">
        {sorted.map((loc) => {
          const { text, cls } = getStatus(loc.risk_level);
          const isHigh = loc.risk_level === "High" || loc.risk_level === "Critical";
          const isCalm = loc.risk_level === "Low";

          return (
            <div
              key={loc.location_id}
              className="ca-card"
              onClick={() => onLocationClick?.(loc)}
            >
              <div className="ca-body">
                <div className="ca-top">
                  <span className="ca-name">{loc.name || `Heritage Site ${loc.location_id}`}</span>
                  <span className={`ca-badge ${cls}`}>{text}</span>
                </div>

                <p className="ca-sub">
                  Tamil Nadu, {loc.visitors ?? Math.floor(Math.random() * 500 + 100)} visitors
                </p>

                {isHigh && (
                  <div className="ca-alert">
                    <AlertTriangle size={14} />
                    <span>Expected congestion today, 8AM – 2PM.</span>
                  </div>
                )}

                <div className="ca-footer">
                  {isHigh && <span className="ca-risk">Risk <strong>HIGH</strong></span>}
                  {isCalm && (
                    <div className="ca-steady-wrap">
                      <span className="ca-steady">✔ STEADY and varies</span>
                      <span className="ca-steady">✔ STEADY and varied</span>
                    </div>
                  )}
                  <button className="ca-btn" onClick={(e) => e.stopPropagation()}>
                    <Navigation size={11} /> Get Directions
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}