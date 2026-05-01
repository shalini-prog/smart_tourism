import { CheckCircle, Bus } from "lucide-react";
import "./HeritageProtection.css";

export default function HeritageProtection() {
  return (
    <div className="heritage-grid">
      <div className="heritage-card white-card">
        <div className="heritage-content">
          <div className="icon-container green-icon">
            <CheckCircle className="icon" />
          </div>
          <div className="text-content">
            <h3 className="card-title">Prioritizing Heritage & User Delivery</h3>
            <p className="card-text">
              Overcrowding reduces the ability to appreciate cultural and artistic value
              causing irreparable damage to historical monuments by accelerating wear and tear.
            </p>
          </div>
        </div>
      </div>

      <div className="heritage-card gradient-card">
        <div className="heritage-content">
          <div className="icon-container white-icon">
            <CheckCircle className="icon" />
          </div>
          <div className="text-content">
            <h3 className="card-title">Protecting Heritage & Promoting Sustainable Tourism</h3>
            <p className="card-text">
              Overcrowding reduced by 42%.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}