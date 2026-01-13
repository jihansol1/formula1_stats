import React from 'react';

const Timeline = ({ races, selectedRace, onRaceSelect }) => {
    return (
        <div className="timeline-container">
            <h2>2024 Season</h2>
            <div className="timeline">
                {races.map((race) => (
                    <div
                        key={race.raceId}
                        className={`timeline-item ${selectedRace?.raceId === race.raceId ? 'selected' : ''}`}
                        onClick={() => onRaceSelect(race)}>

                        <div className="race-round">R{races.indexOf(race) + 1}</div>
                        <div className="race-country">{race.country}</div>
                        <div className="race-date">
                            {new Date(race.date).toLocaleDateString('en-US', {
                                month: 'short',
                                day: 'numeric'
                            })}
                        </div>
                    </div>
                ))}
            </div>
            {selectedRace && (
                <div className="selected-race-info">
                    <h3>{selectedRace.name}</h3>
                    <p>{selectedRace.circuit}</p>
                </div>
            )}
        </div>
    );
};

export default Timeline;