import React, { useState, useEffect } from 'react';
import Timeline from './components/Timeline';
import DriverStandings from './components/DriverStandings';
import ConstructorStandings from './components/ConstructorStandings';
import { getRaces, getDriverStandings, getConstructorStandings } from './services/api';
import './App.css';

function App() {
  const [races, setRaces] = useState([]);
  const [selectedRace, setSelectedRace] = useState(null);
  const [driverStandings, setDriverStandings] = useState([]);
  const [constructorStandings, setConstructorStandings] = useState([]);
  const [loading, setLoading] = useState(true);

  // Load races on mount
  useEffect(() => {
    const fetchRaces = async () => {
      try {
        const data = await getRaces();
        setRaces(data);
        // Select the last race by default
        if (data.length > 0) {
          setSelectedRace(data[data.length - 1]);
        }
      } catch (error) {
        console.error('Error fetching races:', error);
      }
    };
    fetchRaces();
  }, []);

  // Load standings when selected race changes
  useEffect(() => {
    const fetchStandings = async () => {
      if (!selectedRace) return;

      setLoading(true);
      try {
        const [drivers, constructors] = await Promise.all([
          getDriverStandings(selectedRace.raceId),
          getConstructorStandings(selectedRace.raceId)
        ]);
        setDriverStandings(drivers || []);
        setConstructorStandings(constructors || []);
      } catch (error) {
        console.error('Error fetching standings:', error);
        setDriverStandings([]);
        setConstructorStandings([]);
      } finally {
        setLoading(false);
      }
    };
    fetchStandings();
  }, [selectedRace]);

  const handleRaceSelect = (race) => {
    setSelectedRace(race);
  };

  return (
      <div className="app">
        <header className="app-header">
          <h1>🏎️ F1 Stats Dashboard</h1>
          <p>Select a race to see championship standings at that point</p>
        </header>

        <Timeline
            races={races}
            selectedRace={selectedRace}
            onRaceSelect={handleRaceSelect}
        />

        <div className="standings-grid">
          <DriverStandings standings={driverStandings} loading={loading} />
          <ConstructorStandings standings={constructorStandings} loading={loading} />
        </div>
      </div>
  );
}

export default App;