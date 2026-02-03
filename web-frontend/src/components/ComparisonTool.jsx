import React, { useState, useEffect } from 'react';
import { getSummary } from '../services/api';
import axios from 'axios';
import { Radar } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
    Legend
} from 'chart.js';

// Register Chart.js components for radar charts
ChartJS.register(
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
    Legend
);

function ComparisonTool() {
    const [equipment, setEquipment] = useState([]);
    const [selectedIds, setSelectedIds] = useState([]);
    const [comparisonData, setComparisonData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [initialLoading, setInitialLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchEquipment();
    }, []);

    const fetchEquipment = async () => {
        setInitialLoading(true);
        setError('');
        try {
            const data = await getSummary();
            console.log('Summary data:', data);
            if (data.current_dataset && data.current_dataset.equipment) {
                setEquipment(data.current_dataset.equipment);
            } else {
                setError('No equipment data available. Please upload data first.');
            }
        } catch (err) {
            console.error('Error fetching equipment:', err);
            setError('Failed to load equipment data. Please try refreshing the page.');
        } finally {
            setInitialLoading(false);
        }
    };

    const handleSelectionChange = (equipmentId) => {
        if (selectedIds.includes(equipmentId)) {
            setSelectedIds(selectedIds.filter(id => id !== equipmentId));
        } else {
            if (selectedIds.length < 4) {
                setSelectedIds([...selectedIds, equipmentId]);
            } else {
                setError('Maximum 4 equipment can be compared');
            }
        }
    };

    const handleCompare = async () => {
        if (selectedIds.length < 2) {
            setError('Please select at least 2 equipment to compare');
            return;
        }

        setLoading(true);
        setError('');

        try {
            const token = localStorage.getItem('access_token');
            const response = await axios.post(
                'http://localhost:8000/api/compare/',
                { equipment_ids: selectedIds },
                {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                }
            );
            setComparisonData(response.data);
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to compare equipment');
        } finally {
            setLoading(false);
        }
    };

    const getRadarChartData = () => {
        if (!comparisonData) return null;

        const datasets = comparisonData.equipment.map((eq, index) => ({
            label: eq.name,
            data: [
                eq.health_score,
                eq.flowrate,
                eq.pressure,
                eq.temperature,
            ],
            backgroundColor: `rgba(${33 + index * 50}, ${150 + index * 20}, ${243 - index * 30}, 0.2)`,
            borderColor: `rgba(${33 + index * 50}, ${150 + index * 20}, ${243 - index * 30}, 1)`,
            borderWidth: 2,
        }));

        return {
            labels: ['Health Score', 'Flowrate', 'Pressure', 'Temperature'],
            datasets: datasets,
        };
    };

    const radarOptions = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            r: {
                beginAtZero: true,
                ticks: { color: '#4a5568' },
                grid: { color: 'rgba(33, 150, 243, 0.1)' },
            },
        },
        plugins: {
            legend: {
                position: 'top',
                labels: { color: '#1a1a1a' },
            },
            title: {
                display: true,
                text: 'Equipment Performance Comparison',
                color: '#1a1a1a',
                font: { size: 18, weight: 'bold' },
            },
        },
    };

    return (
        <div className="container">
            <h1 style={{ marginBottom: '2rem' }}>Equipment Comparison Tool</h1>

            {initialLoading && (
                <div style={{ textAlign: 'center', padding: '3rem' }}>
                    <div style={{ fontSize: '1.2rem', color: 'var(--text-muted)' }}>
                        Loading equipment data...
                    </div>
                </div>
            )}

            {error && <div className="alert alert-error">{error}</div>}

            {!initialLoading && equipment.length === 0 && !error && (
                <div className="alert alert-warning">
                    No equipment data found. Please upload data from the Upload page first.
                </div>
            )}

            {!initialLoading && equipment.length > 0 && (
                <>
                    <div className="card" style={{ marginBottom: '2rem' }}>
                        <h3 className="card-header">Select Equipment to Compare (2-4)</h3>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', gap: '1rem', padding: '1rem' }}>
                            {equipment.map((eq) => (
                                <label
                                    key={eq.id}
                                    style={{
                                        display: 'flex',
                                        alignItems: 'center',
                                        padding: '0.75rem',
                                        border: selectedIds.includes(eq.id) ? '2px solid var(--accent-primary)' : '1px solid var(--border-color)',
                                        borderRadius: '8px',
                                        cursor: 'pointer',
                                        backgroundColor: selectedIds.includes(eq.id) ? 'var(--bg-hover)' : 'var(--bg-card)',
                                    }}
                                >
                                    <input
                                        type="checkbox"
                                        checked={selectedIds.includes(eq.id)}
                                        onChange={() => handleSelectionChange(eq.id)}
                                        style={{ marginRight: '0.5rem' }}
                                    />
                                    <div>
                                        <div style={{ fontWeight: 'bold' }}>{eq.name}</div>
                                        <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                                            {eq.equipment_type} | Health: {eq.health_score.toFixed(1)}
                                        </div>
                                    </div>
                                </label>
                            ))}
                        </div>

                        <div style={{ padding: '1rem', textAlign: 'center' }}>
                            <button
                                onClick={handleCompare}
                                disabled={selectedIds.length < 2 || loading}
                                className="btn btn-primary"
                                style={{ padding: '0.75rem 2rem' }}
                            >
                                {loading ? 'Comparing...' : `Compare ${selectedIds.length} Equipment`}
                            </button>
                        </div>
                    </div>
                </>
            )}

            {comparisonData && (
                <>
                    {/* Radar Chart */}
                    <div className="card" style={{ marginBottom: '2rem' }}>
                        <div style={{ height: '400px', padding: '1rem' }}>
                            <Radar data={getRadarChartData()} options={radarOptions} />
                        </div>
                    </div>

                    {/* Comparison Metrics */}
                    <div className="card" style={{ marginBottom: '2rem' }}>
                        <h3 className="card-header">Comparison Summary</h3>
                        <div style={{ padding: '1rem' }}>
                            <div className="grid grid-3">
                                <div className="stat-card">
                                    <div className="stat-value">{comparisonData.comparison_metrics.avg_health_score.toFixed(1)}</div>
                                    <div className="stat-label">Average Health Score</div>
                                </div>
                                <div className="stat-card">
                                    <div className="stat-value stat-healthy">{comparisonData.comparison_metrics.best_performer}</div>
                                    <div className="stat-label">Best Performer</div>
                                </div>
                                <div className="stat-card">
                                    <div className="stat-value stat-critical">{comparisonData.comparison_metrics.worst_performer}</div>
                                    <div className="stat-label">Needs Attention</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Detailed Comparison Table */}
                    <div className="card">
                        <h3 className="card-header">Detailed Comparison</h3>
                        <div className="table-container">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Equipment</th>
                                        <th>Type</th>
                                        <th>Health Score</th>
                                        <th>Flowrate</th>
                                        <th>Pressure</th>
                                        <th>Temperature</th>
                                        <th>Risk Level</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {comparisonData.equipment.map((eq) => (
                                        <tr key={eq.id}>
                                            <td><strong>{eq.name}</strong></td>
                                            <td>{eq.equipment_type}</td>
                                            <td>{eq.health_score.toFixed(1)}</td>
                                            <td>{eq.flowrate.toFixed(2)}</td>
                                            <td>{eq.pressure.toFixed(2)}</td>
                                            <td>{eq.temperature.toFixed(2)}°C</td>
                                            <td>
                                                <span className={`badge badge-${eq.risk_level.toLowerCase()}`}>
                                                    {eq.risk_level}
                                                </span>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </>
            )}
        </div>
    );
}

export default ComparisonTool;
