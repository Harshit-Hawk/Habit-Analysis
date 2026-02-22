import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Activity, BarChart2, PlusCircle } from 'lucide-react';
import HabitList from './components/HabitList';
import LogHabitForm from './components/LogHabitForm';
import AnalyticsView from './components/AnalyticsView';

function App() {
  return (
    <Router>
      <div className="app-container">
        <nav className="sidebar">
          <div className="sidebar-header">
            <Activity className="logo-icon" />
            <h2>Habit AI</h2>
          </div>
          <ul className="nav-links">
            <li>
              <Link to="/">
                <BarChart2 size={20} />
                <span>Dashboard</span>
              </Link>
            </li>
            <li>
              <Link to="/habits">
                <Activity size={20} />
                <span>Habits</span>
              </Link>
            </li>
            <li>
              <Link to="/log">
                <PlusCircle size={20} />
                <span>Log Activity</span>
              </Link>
            </li>
          </ul>
        </nav>
        
        <main className="main-content">
          <Routes>
            <Route path="/" element={<AnalyticsView />} />
            <Route path="/habits" element={<HabitList />} />
            <Route path="/log" element={<LogHabitForm />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
