import React, { useState, useEffect } from 'react';
import API_BASE_URL from '../config';

function ActivitiesList() {
  const [activities, setActivities] = useState([]);
  const [selectedType, setSelectedType] = useState('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const activityTypes = ['running', 'cycling', 'swimming', 'weight_training', 'yoga'];

  useEffect(() => {
    fetchActivities();
  }, [selectedType]);

  const fetchActivities = async () => {
    try {
      setLoading(true);
      let url = `${API_BASE_URL}/activities/`;
      if (selectedType !== 'all') {
        url = `${API_BASE_URL}/activities/by_type/?type=${selectedType}`;
      }
      const response = await fetch(url);
      if (!response.ok) throw new Error('Failed to fetch activities');
      const data = await response.json();
      setActivities(data.slice(0, 20)); // Show first 20 activities
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getActivityIcon = (type) => {
    const icons = {
      running: '🏃',
      cycling: '🚴',
      swimming: '🏊',
      weight_training: '🏋️',
      yoga: '🧘'
    };
    return icons[type] || '💪';
  };

  if (loading) return <div className="loading">⏳ Loading activities...</div>;
  if (error) return <div className="error">❌ Error: {error}</div>;

  return (
    <div className="activities-container">
      <h2>🏃 Recent Activities</h2>
      
      <div className="activity-filter">
        <button 
          className={selectedType === 'all' ? 'active' : ''} 
          onClick={() => setSelectedType('all')}
        >
          All Activities
        </button>
        {activityTypes.map(type => (
          <button 
            key={type}
            className={selectedType === type ? 'active' : ''} 
            onClick={() => setSelectedType(type)}
          >
            {getActivityIcon(type)} {type.replace('_', ' ')}
          </button>
        ))}
      </div>

      <div className="activities-list">
        {activities.map((activity, idx) => (
          <div key={idx} className="activity-card">
            <div className="activity-header">
              <h3>{getActivityIcon(activity.activity_type)} {activity.user_name}</h3>
              <span className="activity-type">{activity.activity_type}</span>
            </div>
            <div className="activity-stats">
              <span className="stat">📍 {activity.distance.toFixed(2)} km</span>
              <span className="stat">⏱️ {activity.duration} min</span>
              <span className="stat">🔥 {activity.calories_burned} cal</span>
              <span className={`intensity ${activity.intensity}`}>
                {activity.intensity.toUpperCase()}
              </span>
            </div>
            <p className="date">
              📅 {new Date(activity.date).toLocaleDateString()}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ActivitiesList;
