import { useEffect, useMemo, useState } from "react";
import monsteraImg from "./assets/monstera.jpg";
import snakePlantImg from "./assets/snakeplant.jpg";
import peaceLilyImg from "./assets/peacelily.jpg";
import pothosImg from "./assets/pothos.jpg";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState("");
  const [searchTerm, setSearchTerm] = useState("");

  const [apiPlants, setApiPlants] = useState([]);
  const [selectedPlant, setSelectedPlant] = useState(null);
  const [selectedPlantStatus, setSelectedPlantStatus] = useState(null);

  const [loadingPlants, setLoadingPlants] = useState(false);
  const [loadingStatus, setLoadingStatus] = useState(false);
  const [error, setError] = useState("");

  const getPlantImage = (name = "", type = "") => {
    const value = `${name} ${type}`.toLowerCase();

    if (value.includes("monstera")) return monsteraImg;
    if (value.includes("snake")) return snakePlantImg;
    if (value.includes("peace")) return peaceLilyImg;
    if (value.includes("pothos")) return pothosImg;

    return pothosImg;
  };

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

  const filteredPlants = browsePlants.filter((plant) =>
    plant.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  useEffect(() => {
    if (!isLoggedIn) return;

    setLoadingPlants(true);
    setError("");

    fetch("http://127.0.0.1:8000/api/plants")
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to load plants");
        }
        return res.json();
      })
      .then((data) => {
        setApiPlants(data);

        if (data.length > 0) {
          const firstPlant = data[0];
          setSelectedPlant({
            id: firstPlant.uuid || firstPlant.plant_id,
            source: "myPlants",
            name: firstPlant.plant_name || firstPlant.nickname || "My Plant",
            type: firstPlant.species_id || "Plant",
            image: getPlantImage(firstPlant.plant_name, firstPlant.species_id),
          });
        }
      })
      .catch((err) => {
        setError(err.message);
      })
      .finally(() => {
        setLoadingPlants(false);
      });
  }, [isLoggedIn]);

  useEffect(() => {
    if (!selectedPlant) return;
    if (selectedPlant.source !== "myPlants") return;

    setLoadingStatus(true);
    setError("");

    fetch(
      `http://127.0.0.1:8000/api/plants/${selectedPlant.id}/status?audience_level=beginner`
    )
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to load plant status");
        }
        return res.json();
      })
      .then((data) => {
        setSelectedPlantStatus(data);
      })
      .catch((err) => {
        setError(err.message);
        setSelectedPlantStatus(null);
      })
      .finally(() => {
        setLoadingStatus(false);
      });
  }, [selectedPlant]);

  const myPlants = useMemo(() => {
    return apiPlants.map((plant) => ({
      id: plant.uuid || plant.plant_id,
      source: "myPlants",
      name: plant.plant_name || plant.nickname || "My Plant",
      type: plant.species_id || "Plant",
      image: getPlantImage(plant.plant_name, plant.species_id),
      status: "Tap to view live status",
    }));
  }, [apiPlants]);

  const detailData = useMemo(() => {
    if (!selectedPlant) return null;

    if (selectedPlant.source === "browse") {
      return {
        ...selectedPlant,
        current: {
          water: "Not yet scanned",
          light: "Not yet scanned",
          humidity: "Not yet scanned",
          temperature: "Not yet scanned",
        },
      };
    }

    if (!selectedPlantStatus) {
      return {
        ...selectedPlant,
        current: {
          water: loadingStatus ? "Loading..." : "Unavailable",
          light: loadingStatus ? "Loading..." : "Unavailable",
          humidity: loadingStatus ? "Loading..." : "Unavailable",
          temperature: loadingStatus ? "Loading..." : "Unavailable",
        },
        ideal: {
          water: "Loading...",
          light: "Loading...",
          humidity: "Loading...",
          temperature: "Loading...",
        },
        status: loadingStatus ? "Loading recommendation..." : "No data available.",
      };
    }

    const speciesName = (selectedPlantStatus.species || "").toLowerCase();
    const browseMatch = browsePlants.find(
      (plant) => plant.name.toLowerCase() === speciesName
    );

    return {
      ...selectedPlant,
      name: selectedPlantStatus.plant_name,
      type: selectedPlantStatus.species,
      image: getPlantImage(selectedPlantStatus.plant_name, selectedPlantStatus.species),
      current: {
        water: `${selectedPlantStatus.sensors?.moisture ?? "N/A"}% soil moisture`,
        light: `${selectedPlantStatus.sensors?.light ?? "N/A"} lux`,
        humidity: `${selectedPlantStatus.sensors?.humidity ?? "N/A"}%`,
        temperature: `${selectedPlantStatus.sensors?.temperature ?? "N/A"}°C`,
      },
      ideal: browseMatch
        ? browseMatch.ideal
        : {
            water: "See species profile",
            light: "See species profile",
            humidity: "See species profile",
            temperature: "See species profile",
          },
      status:
        selectedPlantStatus.recommendation?.text ||
        selectedPlantStatus.health_status ||
        "No recommendation available.",
      healthStatus: selectedPlantStatus.health_status,
      healthScore: selectedPlantStatus.health_score,
      alerts: selectedPlantStatus.alerts || [],
    };
  }, [selectedPlant, selectedPlantStatus, browsePlants, loadingStatus]);

  if (!isLoggedIn) {
    return (
      <div className="app-shell">
        <div className="login-card">
          <div className="brand-block">
            <p className="brand-kicker">Smart indoor plant care</p>
            <h1 className="brand-title">FloraSense</h1>
            <p className="app-subtitle">
              Scan plants, monitor conditions, and view the care insights they need
              to stay healthy.
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
            Don’t have an account?{" "}
            <span className="create-account-link">Create Account</span>
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
            <h1 className="dashboard-title">{username ? username : "Guest"}</h1>
          </div>
          <button className="settings-btn">⚙</button>
        </div>

        {error && (
          <div className="section-block">
            <p style={{ color: "#ffb3b3" }}>Error: {error}</p>
          </div>
        )}

        <div className="scan-card">
          <div>
            <p className="small-label">Quick Action</p>
            <h2>Scan Your Plant</h2>
            <p className="scan-text">
              Use your camera to capture a plant image for identification and future
              care analysis.
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
                className={`browse-card ${
                  selectedPlant?.name === plant.name ? "selected-card" : ""
                }`}
                key={plant.id}
                onClick={() =>
                  setSelectedPlant({
                    id: plant.id,
                    source: "browse",
                    name: plant.name,
                    type: plant.name,
                    image: plant.image,
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

          {loadingPlants ? (
            <p>Loading your plants...</p>
          ) : myPlants.length === 0 ? (
            <p>No plants found.</p>
          ) : (
            <div className="my-plants-list">
              {myPlants.map((plant) => (
                <div
                  key={plant.id}
                  className={`my-plant-card ${
                    selectedPlant?.id === plant.id && selectedPlant?.source === "myPlants"
                      ? "selected-card"
                      : ""
                  }`}
                  onClick={() => setSelectedPlant(plant)}
                >
                  <img src={plant.image} alt={plant.name} />
                  <div className="my-plant-info">
                    <h3>{plant.name}</h3>
                    <p>{plant.type}</p>
                    <span>
                      {selectedPlant?.id === plant.id &&
                      selectedPlant?.source === "myPlants" &&
                      selectedPlantStatus?.recommendation?.text
                        ? selectedPlantStatus.recommendation.text
                        : plant.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="section-block">
          <h2 className="section-title">Plant Details</h2>

          {detailData && (
            <div className="detail-card">
              <img
                src={detailData.image}
                alt={detailData.name}
                className="detail-image"
              />
              <h3>{detailData.name}</h3>
              <p className="detail-type">{detailData.type}</p>

              <div className="info-tag">
                {detailData.source === "myPlants"
                  ? "Monitored plant with current sensor readings"
                  : "General plant profile with recommended care conditions"}
              </div>

              {detailData.healthStatus && (
                <div className="info-tag" style={{ marginTop: "0.75rem" }}>
                  {detailData.healthStatus} · Score {detailData.healthScore}
                </div>
              )}

              <div className="detail-grid">
                <div className="mini-box">
                  <h4>Current Water</h4>
                  <p>{detailData.current.water}</p>
                </div>
                <div className="mini-box">
                  <h4>Current Light</h4>
                  <p>{detailData.current.light}</p>
                </div>
                <div className="mini-box">
                  <h4>Current Humidity</h4>
                  <p>{detailData.current.humidity}</p>
                </div>
                <div className="mini-box">
                  <h4>Current Temperature</h4>
                  <p>{detailData.current.temperature}</p>
                </div>
              </div>

              <div className="ideal-box">
                <h4>Ideal Conditions</h4>
                <p><strong>Water:</strong> {detailData.ideal.water}</p>
                <p><strong>Light:</strong> {detailData.ideal.light}</p>
                <p><strong>Humidity:</strong> {detailData.ideal.humidity}</p>
                <p><strong>Temperature:</strong> {detailData.ideal.temperature}</p>
              </div>

              <div className="status-box">
                <h4>Recommendation</h4>
                <p>{detailData.status}</p>
              </div>

              {detailData.source === "myPlants" && detailData.alerts?.length > 0 && (
                <div className="status-box">
                  <h4>Alerts</h4>
                  {detailData.alerts.map((alert, index) => (
                    <p key={index}>
                      {alert.message} — {alert.action}
                    </p>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;