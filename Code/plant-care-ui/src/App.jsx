import { useState } from "react";
import monsteraImg from "./assets/monstera.jpg";
import snakePlantImg from "./assets/snakeplant.jpg";
import peaceLilyImg from "./assets/peacelily.jpg";
import pothosImg from "./assets/pothos.jpg";

function App() {
const [isLoggedIn, setIsLoggedIn] = useState(false);
const [username, setUsername] = useState("");
const [searchTerm, setSearchTerm] = useState("");

  const browsePlants = [
    {
      id: 1,
      name: "Monstera",
      description: "Thrives in warm indoor spaces with moderate moisture.",
      image: monsteraImg,
      ideal: {
        water: "40–60% soil moisture",
        light: "500–1000 lux",
        humidity: "50–70%",
        temperature: "18–27°C",
      },
    },
    {
      id: 2,
      name: "Snake Plant",
      description: "Very resilient and suitable for beginners.",
      image: snakePlantImg,
      ideal: {
        water: "30–50% soil moisture",
        light: "200–800 lux",
        humidity: "30–50%",
        temperature: "18–30°C",
      },
    },
    {
      id: 3,
      name: "Peace Lily",
      description: "Prefers humid conditions and evenly moist soil.",
      image: peaceLilyImg,
      ideal: {
        water: "45–65% soil moisture",
        light: "200–700 lux",
        humidity: "50–80%",
        temperature: "18–26°C",
      },
    },
    {
      id: 4,
      name: "Pothos",
      description: "Low-maintenance plant that adapts well indoors.",
      image: pothosImg,
      ideal: {
        water: "35–55% soil moisture",
        light: "300–800 lux",
        humidity: "40–60%",
        temperature: "18–29°C",
      },
    },
  ];

  const myPlants = [
    {
      id: 101,
      source: "myPlants",
      name: "Living Room Monstera",
      type: "Monstera",
      image: monsteraImg,
      current: {
        water: "32% soil moisture",
        light: "520 lux",
        humidity: "46%",
        temperature: "24°C",
      },
      ideal: {
        water: "40–60% soil moisture",
        light: "500–1000 lux",
        humidity: "50–70%",
        temperature: "18–27°C",
      },
      status: "Slightly dry. Water soon.",
    },
    {
      id: 102,
      source: "myPlants",
      name: "Bedroom Snake Plant",
      type: "Snake Plant",
      image: snakePlantImg,
      current: {
        water: "58% soil moisture",
        light: "300 lux",
        humidity: "41%",
        temperature: "23°C",
      },
      ideal: {
        water: "30–50% soil moisture",
        light: "200–800 lux",
        humidity: "30–50%",
        temperature: "18–30°C",
      },
      status: "Healthy. No action needed.",
    },
    {
      id: 103,
      source: "myPlants",
      name: "Desk Pothos",
      type: "Pothos",
      image: pothosImg,
      current: {
        water: "37% soil moisture",
        light: "410 lux",
        humidity: "49%",
        temperature: "22°C",
      },
      ideal: {
        water: "35–55% soil moisture",
        light: "300–800 lux",
        humidity: "40–60%",
        temperature: "18–29°C",
      },
      status: "Stable. Continue monitoring.",
    },
  ];

  const [selectedPlant, setSelectedPlant] = useState(myPlants[0]);

  const filteredPlants = browsePlants.filter((plant) =>
    plant.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (!isLoggedIn) {
    return (
      <div className="app-shell">
        <div className="login-card">
          <div className="brand-block">
  <p className="brand-kicker">Smart indoor plant care</p>
  <h1 className="brand-title">FloraSense</h1>
  <p className="app-subtitle">
    Scan plants, monitor conditions, and view the care insights they need to stay healthy.
  </p>
</div>

          <input
  type="text"
  placeholder="Username"
  className="input-field"
  value={username}
  onChange={(e) => setUsername(e.target.value)}
/>
<input type="password" placeholder="Password" className="input-field" />

<button className="primary-btn" onClick={() => setIsLoggedIn(true)}>
  Login
</button>
<button className="secondary-btn" onClick={() => setIsLoggedIn(true)}>
  Continue as Guest
</button>

<p className="create-account-text">
  Don’t have an account? <span className="create-account-link">Create Account</span>
</p>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-shell">
      <div className="dashboard-container">
        <div className="dashboard-topbar">
  <div>
    <p className="welcome-text">Welcome back</p>
    <h1 className="dashboard-title">
      {username ? username : "Guest"}
    </h1>
  </div>
  <button className="settings-btn">⚙</button>
</div>

        <div className="scan-card">
          <div>
            <p className="small-label">Quick Action</p>
            <h2>Scan Your Plant</h2>
            <p className="scan-text">
              Use your camera to capture a plant image for identification and future care analysis.
            </p>
          </div>

          <div className="scan-actions">
            <button className="primary-btn small-btn">Open Camera</button>
            <button className="secondary-btn small-btn">Upload Image</button>
          </div>
        </div>

        <div className="section-block">
          <h2 className="section-title">Search Plant</h2>
          <input
            type="text"
            className="input-field"
            placeholder="Search for a plant..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <div className="section-block">
          <h2 className="section-title">Browse Plants</h2>
          <div className="horizontal-scroll">
            {filteredPlants.map((plant) => (
              <div
                className={`browse-card ${selectedPlant.name === plant.name ? "selected-card" : ""}`}
                key={plant.id}
                onClick={() =>
                  setSelectedPlant({
                    id: plant.id,
                    source: "browse",
                    name: plant.name,
                    type: plant.name,
                    image: plant.image,
                    current: {
                      water: "Not yet scanned",
                      light: "Not yet scanned",
                      humidity: "Not yet scanned",
                      temperature: "Not yet scanned",
                    },
                    ideal: plant.ideal,
                    status: plant.description,
                  })
                }
              >
                <img src={plant.image} alt={plant.name} className="browse-img" />
                <h3>{plant.name}</h3>
                <p>{plant.description}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="section-block">
          <h2 className="section-title">My Plants</h2>
          <div className="my-plants-list">
            {myPlants.map((plant) => (
              <div
                key={plant.id}
                className={`my-plant-card ${selectedPlant.id === plant.id ? "selected-card" : ""}`}
                onClick={() => setSelectedPlant(plant)}
              >
                <img src={plant.image} alt={plant.name} />
                <div className="my-plant-info">
                  <h3>{plant.name}</h3>
                  <p>{plant.type}</p>
                  <span>{plant.status}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="section-block">
          <h2 className="section-title">Plant Details</h2>
          <div className="detail-card">
            <img src={selectedPlant.image} alt={selectedPlant.name} className="detail-image" />
            <h3>{selectedPlant.name}</h3>
            <p className="detail-type">{selectedPlant.type}</p>

            <div className="info-tag">
              {selectedPlant.source === "myPlants"
                ? "Monitored plant with current sensor readings"
                : "General plant profile with recommended care conditions"}
            </div>

            <div className="detail-grid">
              <div className="mini-box">
                <h4>Current Water</h4>
                <p>{selectedPlant.current.water}</p>
              </div>
              <div className="mini-box">
                <h4>Current Light</h4>
                <p>{selectedPlant.current.light}</p>
              </div>
              <div className="mini-box">
                <h4>Current Humidity</h4>
                <p>{selectedPlant.current.humidity}</p>
              </div>
              <div className="mini-box">
                <h4>Current Temperature</h4>
                <p>{selectedPlant.current.temperature}</p>
              </div>
            </div>

            <div className="ideal-box">
              <h4>Ideal Conditions</h4>
              <p><strong>Water:</strong> {selectedPlant.ideal.water}</p>
              <p><strong>Light:</strong> {selectedPlant.ideal.light}</p>
              <p><strong>Humidity:</strong> {selectedPlant.ideal.humidity}</p>
              <p><strong>Temperature:</strong> {selectedPlant.ideal.temperature}</p>
            </div>

            <div className="status-box">
              <h4>Recommendation</h4>
              <p>{selectedPlant.status}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;