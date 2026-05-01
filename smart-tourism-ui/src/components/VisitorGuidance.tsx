import { XCircle, Smile, ArrowRight } from "lucide-react";
import "./VisitorGuidance.css";

interface Advisory {
  location_id: number;
  current_status: string;
  trend: string;
  best_time_to_visit: string;
  weather_summary: string;
  comfort_score: number;
  final_recommendation: string;
}

interface VisitorGuidanceProps {
  selectedLocation: any;
  advisory: Advisory | null;
}

export default function VisitorGuidance({ selectedLocation, advisory }: VisitorGuidanceProps) {
  const recommendations = advisory ? [
    {
      type: advisory.current_status.includes("Crowded") ? "avoid" : "visit",
      icon: advisory.current_status.includes("Crowded") ? XCircle : Smile,
      text: advisory.final_recommendation || "Check current conditions",
      color: advisory.current_status.includes("Crowded") ? "red" : "blue"
    }
  ] : [
    {
      type: "avoid",
      icon: XCircle,
      text: "Avoid Meenakshi Temple until after 3 PM",
      color: "red",
      image: "https://images.pexels.com/photos/3290068/pexels-photo-3290068.jpeg?auto=compress&cs=tinysrgb&w=100"
    },
    {
      type: "visit",
      icon: Smile,
      text: "Visit Ramanathasswamy Temple for a calmer experience",
      color: "blue",
      image: "https://images.pexels.com/photos/3293148/pexels-photo-3293148.jpeg?auto=compress&cs=tinysrgb&w=100"
    },
    {
      type: "alternative",
      icon: ArrowRight,
      text: "Consider Koodal Azhagar Temple as an alternative",
      color: "green",
      image: "https://images.pexels.com/photos/3661263/pexels-photo-3661263.jpeg?auto=compress&cs=tinysrgb&w=100"
    }
  ];

  return (
    <div className="guidance-container">
      <h2 className="guidance-title">Visitor Guidance & Recommendations</h2>

      <div className="recommendations-list">
        {recommendations.map((rec, index) => (
          <div key={index} className="recommendation-item">
            <div className={`recommendation-icon ${rec.color}`}>
              {rec.image ? (
                <img src={rec.image} alt="" className="recommendation-image" />
              ) : (
                <rec.icon className="icon-svg" />
              )}
            </div>
            <p className="recommendation-text">{rec.text}</p>
          </div>
        ))}
      </div>

      {advisory && (
        <div className="advisory-details">
          <div className="advisory-grid">
            <div className="advisory-item">
              <p className="advisory-label">Best Time</p>
              <p className="advisory-value">{advisory.best_time_to_visit}</p>
            </div>
            <div className="advisory-item">
              <p className="advisory-label">Comfort Score</p>
              <p className="advisory-value">{advisory.comfort_score}/100</p>
            </div>
            <div className="advisory-item advisory-full">
              <p className="advisory-label">Weather</p>
              <p className="advisory-value">{advisory.weather_summary}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}