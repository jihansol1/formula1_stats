import React, { useState, useEffect } from 'react';
import Timeline from './components/Timeline';
import DriverStandings from './components/DriverStandings';
import ConstructorStandings from './components/ConstructorStandings';
import SeasonSelector from './components/SeasonSelector';
import { getSeasons, getRacesBySeason, getDriverStandings, getConstructorStandings } from './services/api';
import './App.css';

function App() {
  const [seasons, setSeasons] = useState([]);
  const [selectedSeason, setSelectedSeason] = useState(null);
  const [races, setRaces] = useState([]);
  const [selectedRace, setSelectedRace] = useState(null);
  const [driverStandings, setDriverStandings] = useState([]);
  const [constructorStandings, setConstructorStandings] = useState([]);
  const [loading, setLoading] = useState(true);

  // Load seasons on mount
  useEffect(() => {
    const fetchSeasons = async () => {
      try {
        const data = await getSeasons();
        setSeasons(data);
        if (data.length > 0) {
          setSelectedSeason(data[0]); // Most recent season
        }
      } catch (error) {
        console.error('Error fetching seasons:', error);
      }
    };
    fetchSeasons();
  }, []);

  // Load races when season changes
  useEffect(() => {
    const fetchRaces = async () => {
      if (!selectedSeason) return;

      try {
        const data = await getRacesBySeason(selectedSeason);
        setRaces(data);
        if (data.length > 0) {
          setSelectedRace(data[data.length - 1]); // Last race of season
        }
      } catch (error) {
        console.error('Error fetching races:', error);
      }
    };
    fetchRaces();
  }, [selectedSeason]);

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
        setDriverStandings(drivers);
        setConstructorStandings(constructors);
      } catch (error) {
        console.error('Error fetching standings:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchStandings();
  }, [selectedRace]);

  const handleSeasonChange = (season) => {
    setSelectedSeason(season);
    setSelectedRace(null);
    setDriverStandings([]);
    setConstructorStandings([]);
  };

  const handleRaceSelect = (race) => {
    setSelectedRace(race);
  };

  return (
      <div className="app">
        <header className="app-header">
          <h1>🏎️ F1 Stats Dashboard</h1>
          <p>Select a season and race to see championship standings</p>
        </header>

        <SeasonSelector
            seasons={seasons}
            selectedSeason={selectedSeason}
            onSeasonChange={handleSeasonChange}
        />

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