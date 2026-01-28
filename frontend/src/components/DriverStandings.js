import React from 'react';

const DriverStandings = ({ standings, loading }) => {
    if (loading) {
        return <div className="loading">Loading standings...</div>;
    }

    if (!standings || standings.length === 0) {
        return (
            <div className="standings-container">
                <h2>Driver Standings</h2>
                <div className="no-data">No standings data available</div>
            </div>
        );
    }

    return (
        <div className="standings-container">
            <h2>Driver Standings</h2>
            <table className="standings-table">
                <thead>
                <tr>
                    <th>Pos</th>
                    <th>Driver</th>
                    <th>Team</th>
                    <th>Points</th>
                    <th>Wins</th>
                    <th>Podiums</th>
                </tr>
                </thead>
                <tbody>
                {standings.map((driver) => (
                    <tr key={driver.driverId} className={driver.position <= 3 ? 'podium' : ''}>
                        <td className="position">{driver.position}</td>
                        <td className="driver-name">{driver.name}</td>
                        <td className="team-name">{driver.teamId ? driver.teamId.replace('_', ' ') : ''}</td>
                        <td className="points">{driver.points}</td>
                        <td>{driver.wins}</td>
                        <td>{driver.podiums}</td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
};

export default DriverStandings;