import React, { useState, useEffect } from 'react';
import './App.css';
import UsersList from './components/UsersList';
import ActivitiesList from './components/ActivitiesList';
import LeaderboardView from './components/LeaderboardView';
import API_BASE_URL from './config';

function App() {
  const [activeTab, setActiveTab] = useState('leaderboard');
  const [apiStatus, setApiStatus] = useState('checking');

  useEffect(() => {
    // Check API connection
    console.log('📡 Checking API connection at:', API_BASE_URL);
    fetch(API_BASE_URL)
      .then(res => {
        console.log('✅ API connection successful');
        setApiStatus('connected');
      })
      .catch(err => {
        console.error('❌ API connection failed:', err);
        setApiStatus('disconnected');
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>🏋️ OctoFit Tracker</h1>
        <p>Superhero Fitness Leaderboard</p>
        <div className="api-status">
          Status: <span className={apiStatus}>{apiStatus === 'connected' ? '✅ API Connected' : '⚠️ API Offline'}</span>
        </div>
      </header>

      <nav className="tabs">
        <button 
          className={activeTab === 'leaderboard' ? 'active' : ''} 
          onClick={() => setActiveTab('leaderboard')}
        >
          🏆 Leaderboard
        </button>
        <button 
          className={activeTab === 'users' ? 'active' : ''} 
          onClick={() => setActiveTab('users')}
        >
          👥 Users
        </button>
        <button 
          className={activeTab === 'activities' ? 'active' : ''} 
          onClick={() => setActiveTab('activities')}
        >
          🏃 Activities
        </button>
      </nav>

      <main className="content">
        {activeTab === 'leaderboard' && <LeaderboardView />}
        {activeTab === 'users' && <UsersList />}
        {activeTab === 'activities' && <ActivitiesList />}
      </main>

      <footer>
        <p>OctoFit Tracker © 2026 | Powered by Django & React</p>
      </footer>
    </div>
  );
}

export default App;
