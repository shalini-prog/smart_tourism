import { useState, useEffect } from "react";
import axios from "axios";
import Login from "./components/Login";
import MapView from "./components/MapView";
import CongestionAlerts from "./components/CongestionAlerts";
import VisitorForecast from "./components/VisitorForecast";
import VisitorGuidance from "./components/VisitorGuidance";
import HeritageProtection from "./components/HeritageProtection";
import "./App.css";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [locations, setLocations] = useState([]);
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [advisory, setAdvisory] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!isLoggedIn) return;
    axios
      .get("http://127.0.0.1:8000/predict_all")
      .then((res) => setLocations(res.data.locations))
      .catch((err) => console.error("API Error:", err));
  }, [isLoggedIn]);

  const handleLocationClick = async (location: any) => {
    setSelectedLocation(location);
    setLoading(true);
    setAdvisory(null);
    try {
      const res = await axios.get(
        `http://127.0.0.1:8000/smart_advisory/${location.location_id}`
      );
      setAdvisory(res.data);
    } catch (err) {
      console.error("Advisory API Error:", err);
    } finally {
      setLoading(false);
    }
  };

  // Show Login page until authenticated
  if (!isLoggedIn) {
    return <Login onLogin={() => setIsLoggedIn(true)} />;
  }

  return (
    <div className="app-wrapper">
      {/* Hero Header */}
      <header className="app-header">
        <div className="header-overlay">
          <h1 className="header-title">Tourist Management Dashboard</h1>
          <p className="header-subtitle">
            AI-powered crowd prediction &amp; smart visitor guidance for heritage
            site protection
          </p>
          <button
            className="logout-btn"
            onClick={() => setIsLoggedIn(false)}
            title="Logout"
          >
            ← Logout
          </button>
        </div>
      </header>

      {/* Main Dashboard Grid */}
      <main className="dashboard-main">
        <div className="dashboard-grid">
          {/* Left: Congestion Alerts */}
          <section className="col-left">
            <CongestionAlerts
              locations={locations}
              onLocationClick={handleLocationClick}
            />
          </section>

          {/* Center: Map */}
          <section className="col-center">
            <div className="map-card">
              <h2 className="section-title">Forecasted Crowding Map</h2>
              <div className="map-area">
                <MapView onLocationSelect={handleLocationClick} />
              </div>
            </div>

            {/* Bottom center: Heritage Protection */}
            <HeritageProtection />
          </section>

          {/* Right: Forecast + Guidance */}
          <section className="col-right">
            <VisitorGuidance
              selectedLocation={selectedLocation}
              advisory={advisory}
            />
            <VisitorForecast />
          </section>
        </div>
      </main>
    </div>
  );
}

export default App;