import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import './App.css';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import Upload from './components/Upload';
import History from './components/History';
import ComparisonTool from './components/ComparisonTool';


function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(
        !!localStorage.getItem('access_token')
    );

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setIsAuthenticated(false);
    };

    return (
        <Router>
            {isAuthenticated && (
                <nav className="navbar">
                    <div className="navbar-content">
                        <Link to="/dashboard" className="navbar-brand">
                            Chemical Equipment Intelligence
                        </Link>
                        <div className="navbar-nav">
                            <Link to="/dashboard" className="nav-link">Dashboard</Link>
                            <Link to="/upload" className="nav-link">Upload</Link>
                            <Link to="/comparison" className="nav-link">Comparison</Link>
                            <Link to="/history" className="nav-link">History</Link>
                            <button onClick={handleLogout} className="btn btn-secondary">
                                Logout
                            </button>
                        </div>
                    </div>
                </nav>
            )}

            <Routes>
                <Route
                    path="/login"
                    element={
                        isAuthenticated ?
                            <Navigate to="/dashboard" /> :
                            <Login setIsAuthenticated={setIsAuthenticated} />
                    }
                />
                <Route
                    path="/dashboard"
                    element={
                        isAuthenticated ?
                            <Dashboard /> :
                            <Navigate to="/login" />
                    }
                />
                <Route
                    path="/upload"
                    element={
                        isAuthenticated ?
                            <Upload onUploadSuccess={() => window.location.href = '/dashboard'} /> :
                            <Navigate to="/login" />
                    }
                />
                <Route
                    path="/comparison"
                    element={
                        isAuthenticated ?
                            <ComparisonTool /> :
                            <Navigate to="/login" />
                    }
                />
                <Route
                    path="/history"
                    element={
                        isAuthenticated ?
                            <History /> :
                            <Navigate to="/login" />
                    }
                />
                <Route path="/" element={<Navigate to="/dashboard" />} />
            </Routes>
        </Router>
    );
}

export default App;
