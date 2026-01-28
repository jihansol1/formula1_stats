import React from 'react';

const Timeline = ({ races, selectedRace, onRaceSelect }) => {
    if (!races || races.length === 0) {
        return <div className="timeline-container"><p>Loading races...</p></div>;
    }

    const season = races[0]?.season;

    return (
        <div className="timeline-container">
            <h2>{season} Season</h2>
            <div className="timeline">
                {races.map((race, index) => (
                    <div
                        key={race.raceId}
                        className={`timeline-item ${selectedRace?.raceId === race.raceId ? 'selected' : ''}`}
                        onClick={() => onRaceSelect(race)}
                    >
                        <div className="race-round">R{index + 1}</div>
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