import React, { useState, useEffect } from 'react';
import api from '../api';

const LogHabitForm = () => {
  const [habits, setHabits] = useState([]);
  const [selectedHabitId, setSelectedHabitId] = useState('');
  const [status, setStatus] = useState('success');
  const [sleepHours, setSleepHours] = useState(7);
  const [mood, setMood] = useState('neutral');
  const [context, setContext] = useState('work');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchHabits = async () => {
      try {
        const response = await api.get('/habits/');
        setHabits(response.data);
        if (response.data.length > 0) {
          setSelectedHabitId(response.data[0].id);
        }
      } catch (error) {
        console.error("Error fetching habits", error);
      }
    };
    fetchHabits();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedHabitId) return;

    setLoading(true);
    setMessage('');
    
    try {
      await api.post('/logs/', {
        habit_id: parseInt(selectedHabitId),
        status: status,
        sleep_hours: parseFloat(sleepHours),
        mood: mood,
        context: context
      });
      setMessage('Successfully logged!');
      setTimeout(() => setMessage(''), 3000); // Clear message
    } catch (error) {
      console.error("Error logging habit", error);
      setMessage('Failed to log habit.');
    } finally {
      setLoading(false);
    }
  };

  if (habits.length === 0) {
    return (
      <div className="card">
        <h2>Log Activity</h2>
        <p className="no-data">Please create a habit first before logging.</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h2>Log Activity</h2>
      {message && <div className={`alert ${message.includes('Success') ? 'alert-success' : 'alert-error'}`}>{message}</div>}
      
      <form onSubmit={handleSubmit} className="log-form">
        <div className="form-group">
          <label>Habit</label>
          <select 
            value={selectedHabitId}
            onChange={(e) => setSelectedHabitId(e.target.value)}
            className="form-select full-width"
          >
            {habits.map(h => (
              <option key={h.id} value={h.id}>{h.name}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Outcome</label>
          <div className="button-group">
            <button 
              type="button" 
              className={`btn ${status === 'success' ? 'btn-success' : 'btn-outline'}`}
              onClick={() => setStatus('success')}
            >
              Success
            </button>
            <button 
              type="button" 
              className={`btn ${status === 'failure' ? 'btn-error' : 'btn-outline'}`}
              onClick={() => setStatus('failure')}
            >
              Failure
            </button>
          </div>
        </div>

        <div className="form-group">
          <label>Sleep (Hours: {sleepHours})</label>
          <input 
            type="range" 
            min="0" max="14" step="0.5"
            value={sleepHours}
            onChange={(e) => setSleepHours(e.target.value)}
            className="form-range"
          />
        </div>

        <div className="form-row">
          <div className="form-group split">
            <label>Mood</label>
            <select 
              value={mood}
              onChange={(e) => setMood(e.target.value)}
              className="form-select full-width"
            >
              <option value="stressed">Stressed</option>
              <option value="tired">Tired</option>
              <option value="distracted">Distracted</option>
              <option value="neutral">Neutral</option>
            </select>
          </div>

          <div className="form-group split">
            <label>Context</label>
            <select 
              value={context}
              onChange={(e) => setContext(e.target.value)}
              className="form-select full-width"
            >
              <option value="phone">Phone/Screen</option>
              <option value="work">Work/Study</option>
              <option value="social">Social</option>
              <option value="other">Other</option>
            </select>
          </div>
        </div>

        <button type="submit" disabled={loading} className="btn btn-primary full-width mt-4">
          Save Log
        </button>
      </form>
    </div>
  );
};

export default LogHabitForm;
