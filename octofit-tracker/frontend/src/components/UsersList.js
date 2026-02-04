import React, { useState, useEffect } from 'react';
import API_BASE_URL from '../config';

function UsersList() {
  const [users, setUsers] = useState([]);
  const [selectedTeam, setSelectedTeam] = useState('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchUsers();
  }, [selectedTeam]);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      let url = `${API_BASE_URL}/users/`;
      if (selectedTeam !== 'all') {
        url += `?team=${encodeURIComponent(selectedTeam)}`;
      }
      const response = await fetch(url);
      if (!response.ok) throw new Error('Failed to fetch users');
      const data = await response.json();
      setUsers(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">⏳ Loading users...</div>;
  if (error) return <div className="error">❌ Error: {error}</div>;

  return (
    <div className="users-container">
      <h2>👥 Superheroes</h2>
      
      <div className="team-filter">
        <button 
          className={selectedTeam === 'all' ? 'active' : ''} 
          onClick={() => setSelectedTeam('all')}
        >
          All Teams
        </button>
        <button 
          className={selectedTeam === 'Team Marvel' ? 'active' : ''} 
          onClick={() => setSelectedTeam('Team Marvel')}
        >
          Team Marvel 🦸
        </button>
        <button 
          className={selectedTeam === 'Team DC' ? 'active' : ''} 
          onClick={() => setSelectedTeam('Team DC')}
        >
          Team DC 🦹
        </button>
      </div>

      <div className="users-grid">
        {users.map((user) => (
          <div key={user.email} className="user-card">
            <h3>{user.name}</h3>
            <p className="team-badge">{user.team}</p>
            <p className="bio">{user.bio}</p>
            <p className="email">📧 {user.email}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default UsersList;
