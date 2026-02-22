import React, { useState, useEffect } from 'react';
import { AlertTriangle, Info, TrendingDown, Clock, MessageSquare, Smartphone } from 'lucide-react';
import api from '../api';

const AnalyticsView = () => {
  const [habits, setHabits] = useState([]);
  const [selectedHabitId, setSelectedHabitId] = useState('');
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(false);

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

  useEffect(() => {
    if (selectedHabitId) {
      fetchAnalytics(selectedHabitId);
    }
  }, [selectedHabitId]);

  const fetchAnalytics = async (habitId) => {
    setLoading(true);
    try {
      const response = await api.get(`/analytics/${habitId}`);
      setAnalytics(response.data);
    } catch (error) {
      console.error("Error fetching analytics", error);
      setAnalytics(null);
    } finally {
      setLoading(false);
    }
  };

  if (habits.length === 0) {
    return (
      <div className="card">
        <h2>Analytics Dashboard</h2>
        <p className="no-data">Create a habit to view analytics.</p>
      </div>
    );
  }

  const renderRiskBadge = (level) => {
    switch(level) {
      case 'High': return <span className="badge badge-high"><AlertTriangle size={14}/> High Risk</span>;
      case 'Medium': return <span className="badge badge-medium">Medium Risk</span>;
      case 'Low': return <span className="badge badge-low">Low Risk</span>;
      default: return null;
    }
  };

  const renderCorrealtions = (title, items, icon) => {
    if (!items || items.length === 0) return null;
    
    return (
      <div className="correlation-group">
        <h4>{icon} {title}</h4>
        <div className="correlation-cards">
          {items.map((stat, idx) => (
            <div key={idx} className="stat-card">
              <span className="stat-factor">{stat.factor}</span>
              <span className="stat-rate">{(stat.failure_rate * 100).toFixed(0)}% fail rate</span>
              <span className="stat-sample">n={stat.sample_size}</span>
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="analytics-container">
      <div className="card header-card">
        <div className="flex-between">
          <h2>Predictive Analytics</h2>
          <select 
            value={selectedHabitId}
            onChange={(e) => setSelectedHabitId(e.target.value)}
            className="form-select min-w-200"
          >
            {habits.map(h => (
              <option key={h.id} value={h.id}>{h.name}</option>
            ))}
          </select>
        </div>
      </div>

      {loading ? (
        <div className="card"><p>Analyzing data...</p></div>
      ) : analytics ? (
        <>
          <div className="card summary-card">
            <div className="summary-stats">
              <div className="stat-box">
                <span className="stat-label">Total Logs</span>
                <span className="stat-value">{analytics.total_logs}</span>
              </div>
              <div className="stat-box">
                <span className="stat-label">Success Rate</span>
                <span className="stat-value">{(analytics.success_rate * 100).toFixed(1)}%</span>
              </div>
              <div className="stat-box">
                <span className="stat-label">Predicted Risk</span>
                <span className="stat-value">{renderRiskBadge(analytics.predictions.risk_level)}</span>
              </div>
            </div>
            
            <div className="ai-insight">
              <h3><Info size={18} /> AI Insight</h3>
              <p>{analytics.predictions.explanation}</p>
            </div>
          </div>

          <div className="card">
            <h3>Failure Correlators (Statistical)</h3>
            <p className="subtitle">Factors detected with high failure probabilities.</p>
            
            <div className="correlations-grid">
              {renderCorrealtions('Mood Impacts', analytics.correlations.mood, <MessageSquare size={16}/>)}
              {renderCorrealtions('Contextual Impacts', analytics.correlations.context, <Smartphone size={16}/>)}
              {renderCorrealtions('Sleep Impacts', analytics.correlations.sleep, <Clock size={16}/>)}
              
              {(!analytics.correlations.mood.length && !analytics.correlations.context.length && !analytics.correlations.sleep.length) && (
                <p className="no-data">Not enough failure data to identify statistical correlations yet.</p>
              )}
            </div>
          </div>
        </>
      ) : (
        <div className="card">
          <p className="no-data">No data available for this habit. Please log some activity first.</p>
        </div>
      )}
    </div>
  );
};

export default AnalyticsView;
