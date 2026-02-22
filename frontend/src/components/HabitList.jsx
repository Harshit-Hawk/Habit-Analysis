import React, { useState, useEffect } from 'react';
import { Trash2 } from 'lucide-react';
import api from '../api';

const HabitList = () => {
  const [habits, setHabits] = useState([]);
  const [newHabitName, setNewHabitName] = useState('');
  const [targetFrequency, setTargetFrequency] = useState('daily');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchHabits();
  }, []);

  const fetchHabits = async () => {
    try {
      const response = await api.get('/habits/');
      setHabits(response.data);
    } catch (error) {
      console.error("Error fetching habits", error);
    }
  };

  const createHabit = async (e) => {
    e.preventDefault();
    if (!newHabitName.trim()) return;

    setLoading(true);
    try {
      await api.post('/habits/', {
        name: newHabitName,
        target_frequency: targetFrequency
      });
      setNewHabitName('');
      fetchHabits();
    } catch (error) {
      console.error("Error creating habit", error);
    } finally {
      setLoading(false);
    }
  };

  const deleteHabit = async (id) => {
    try {
      await api.delete(`/habits/${id}`);
      fetchHabits();
    } catch (error) {
      console.error("Error deleting habit", error);
    }
  };

  return (
    <div className="card">
      <h2>Manage Habits</h2>
      
      <form onSubmit={createHabit} className="create-habit-form">
        <input 
          type="text" 
          placeholder="New habit name..." 
          value={newHabitName}
          onChange={(e) => setNewHabitName(e.target.value)}
          className="form-input"
        />
        <select 
          value={targetFrequency}
          onChange={(e) => setTargetFrequency(e.target.value)}
          className="form-select"
        >
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
        </select>
        <button type="submit" disabled={loading} className="btn btn-primary">
          Add
        </button>
      </form>

      <div className="habit-list">
        {habits.length === 0 ? (
          <p className="no-data">No habits created yet. Add one above!</p>
        ) : (
          habits.map(habit => (
            <div key={habit.id} className="habit-item">
              <div>
                <strong>{habit.name}</strong>
                <span className="badge">{habit.target_frequency}</span>
              </div>
              <button onClick={() => deleteHabit(habit.id)} className="btn-icon">
                <Trash2 size={18} />
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default HabitList;
