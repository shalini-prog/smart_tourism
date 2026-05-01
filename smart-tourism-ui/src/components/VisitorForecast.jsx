import "./VisitorForecast.css";

export default function VisitorForecast() {
  const forecastData = [
    { day: "Tuesday", shortDay: "Tue", visitors: 768, color: "bar-red" },
    { day: "Wednesday", shortDay: "Wed", visitors: 1564, color: "bar-orange" },
    { day: "Thursday", shortDay: "Thu", visitors: 1422, color: "bar-green" },
    { day: "Friday", shortDay: "Fri", visitors: 1422, color: "bar-orange" }
  ];

  const maxVisitors = Math.max(...forecastData.map(d => d.visitors));

  return (
    <div className="forecast-container">
      <h2 className="forecast-title">3-Day Visitor Forecast</h2>

      <div className="forecast-grid">
        {forecastData.map((data, index) => (
          <div key={index} className="forecast-item">
            <div className="forecast-shortday">{data.shortDay}</div>
            <div className="forecast-visitors">{data.visitors}</div>
            <div className="forecast-bar-container">
              <div
                className={`forecast-bar ${data.color}`}
                style={{
                  height: `${(data.visitors / maxVisitors) * 100}%`
                }}
              ></div>
            </div>
            <div className="forecast-day">{data.day}</div>
          </div>
        ))}
      </div>
    </div>
  );
}