import React, { useState, useEffect } from 'react';
import API_BASE_URL from '../config';

function LeaderboardView() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  const fetchLeaderboard = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/leaderboard/top_10/`);
      if (!response.ok) throw new Error('Failed to fetch leaderboard');
      const data = await response.json();
      setLeaderboard(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getMedalEmoji = (rank) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return `#${rank}`;
  };

  if (loading) return <div className="loading">⏳ Loading leaderboard...</div>;
  if (error) return <div className="error">❌ Error: {error}</div>;

  return (
    <div className="leaderboard">
      <h2>🏆 Top 10 Leaderboard</h2>
      <table className="leaderboard-table">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Hero Name</th>
            <th>Team</th>
            <th>Total Activities</th>
            <th>Calories Burned</th>
            <th>Total Distance</th>
          </tr>
        </thead>
        <tbody>
          {leaderboard.map((entry) => (
            <tr key={entry.user_email} className={`rank-${entry.rank}`}>
              <td className="rank-cell">{getMedalEmoji(entry.rank)}</td>
              <td className="hero-name">{entry.user_name}</td>
              <td className={`team ${entry.team.toLowerCase().replace(' ', '-')}`}>
                {entry.team}
              </td>
              <td>{entry.total_activities}</td>
              <td className="calories">🔥 {entry.total_calories_burned}</td>
              <td className="distance">📍 {entry.total_distance.toFixed(2)} km</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default LeaderboardView;
