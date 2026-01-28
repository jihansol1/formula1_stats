import React from 'react';

const SeasonSelector = ({ seasons, selectedSeason, onSeasonChange }) => {
    return (
        <div className="season-selector">
            <label htmlFor="season">Season: </label>
            <select
                id="season"
                value={selectedSeason}
                onChange={(e) => onSeasonChange(Number(e.target.value))}
            >
                {seasons.map(season => (
                    <option key={season} value={season}>{season}</option>
                ))}
            </select>
        </div>
    );
};

export default SeasonSelector;