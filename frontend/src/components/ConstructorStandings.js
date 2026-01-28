import React from 'react';

const ConstructorStandings = ({ standings, loading }) => {
    if (loading) {
        return <div className="loading">Loading standings...</div>;
    }

    if (!standings || standings.length === 0) {
        return (
            <div className="standings-container">
                <h2>Constructor Standings</h2>
                <div className="no-data">No standings data available</div>
            </div>
        );
    }

    return (
        <div className="standings-container">
            <h2>Constructor Standings</h2>
            <table className="standings-table">
                <thead>
                <tr>
                    <th>Pos</th>
                    <th>Team</th>
                    <th>Points</th>
                    <th>Wins</th>
                    <th>Podiums</th>
                </tr>
                </thead>
                <tbody>
                {standings.map((team) => (
                    <tr key={team.teamId} className={team.position <= 3 ? 'podium' : ''}>
                        <td className="position">{team.position}</td>
                        <td className="team-name">{team.name}</td>
                        <td className="points">{team.points}</td>
                        <td>{team.wins}</td>
                        <td>{team.podiums}</td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
};

export default ConstructorStandings;