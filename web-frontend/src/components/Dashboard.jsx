import React, { useState, useEffect } from 'react';
import { getSummary, generateReport } from '../services/api';
import { EquipmentTypeChart, RiskDistributionChart, ParameterTrendsChart } from './Charts';

function Dashboard() {
    const [summary, setSummary] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchSummary();
    }, []);

    const fetchSummary = async () => {
        try {
            setLoading(true);
            const data = await getSummary();
            setSummary(data);
            setError('');
        } catch (err) {
            if (err.response?.status === 404) {
                setError('No data available. Please upload a CSV file first.');
            } else {
                setError('Failed to load summary data');
            }
        } finally {
            setLoading(false);
        }
    };

    const handleDownloadReport = () => {
        if (summary?.current_dataset?.id) {
            const reportUrl = generateReport(summary.current_dataset.id);
            window.open(reportUrl, '_blank');
        }
    };

    const handleExport = async (format) => {
        try {
            const token = localStorage.getItem('access_token');
            const response = await fetch(
                `http://localhost:8000/api/export/${format}/${current_dataset.id}/`,
                {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                }
            );

            if (!response.ok) throw new Error('Export failed');

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `export_${current_dataset.id}.${format === 'excel' ? 'xlsx' : format}`;
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(url);

            // Close menu
            document.getElementById('export-menu').style.display = 'none';
        } catch (error) {
            console.error(`Error exporting to ${format}:`, error);
            alert(`Failed to export to ${format}. Please try again.`);
        }
    };

    if (loading) {
        return (
            <div className="loading">
                <div className="spinner"></div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="container">
                <div className="alert alert-warning">{error}</div>
            </div>
        );
    }

    if (!summary) return null;

    const { current_dataset, trend_comparison, critical_equipment, risk_distribution, parameter_trends } = summary;

    return (
        <div className="container">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h1>Equipment Health Dashboard</h1>
                <div style={{ display: 'flex', gap: '1rem' }}>
                    <button onClick={handleDownloadReport} className="btn btn-primary">
                        Download PDF Report
                    </button>
                    <div style={{ position: 'relative' }}>
                        <button
                            onClick={() => {
                                const menu = document.getElementById('export-menu');
                                menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
                            }}
                            className="btn btn-success"
                        >
                            Export Data ▼
                        </button>
                        <div
                            id="export-menu"
                            style={{
                                display: 'none',
                                position: 'absolute',
                                right: 0,
                                top: '100%',
                                marginTop: '0.5rem',
                                backgroundColor: 'var(--bg-card)',
                                border: '1px solid var(--border-color)',
                                borderRadius: '8px',
                                boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
                                zIndex: 1000,
                                minWidth: '150px'
                            }}
                        >
                            <button
                                onClick={() => handleExport('excel')}
                                style={{
                                    width: '100%',
                                    display: 'block',
                                    padding: '0.75rem 1rem',
                                    backgroundColor: 'transparent',
                                    border: 'none',
                                    borderBottom: '1px solid var(--border-color)',
                                    color: 'var(--text-primary)',
                                    textAlign: 'left',
                                    cursor: 'pointer'
                                }}
                            >
                                📊 Export to Excel
                            </button>
                            <button
                                onClick={() => handleExport('csv')}
                                style={{
                                    width: '100%',
                                    display: 'block',
                                    padding: '0.75rem 1rem',
                                    backgroundColor: 'transparent',
                                    border: 'none',
                                    borderBottom: '1px solid var(--border-color)',
                                    color: 'var(--text-primary)',
                                    textAlign: 'left',
                                    cursor: 'pointer'
                                }}
                            >
                                📄 Export to CSV
                            </button>
                            <button
                                onClick={() => handleExport('json')}
                                style={{
                                    width: '100%',
                                    display: 'block',
                                    padding: '0.75rem 1rem',
                                    backgroundColor: 'transparent',
                                    border: 'none',
                                    color: 'var(--text-primary)',
                                    textAlign: 'left',
                                    cursor: 'pointer'
                                }}
                            >
                                🔧 Export to JSON
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            {/* Executive Summary */}
            <div className="card" style={{ marginBottom: '2rem' }}>
                <h3 className="card-header">Executive Summary</h3>
                <p style={{ lineHeight: '1.8', color: 'var(--text-secondary)' }}>
                    {current_dataset.executive_summary}
                </p>
                <div style={{ marginTop: '1rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                    <strong>Dataset:</strong> {current_dataset.filename} |
                    <strong> Uploaded:</strong> {new Date(current_dataset.upload_date).toLocaleString()}
                </div>
            </div>

            {/* Summary Statistics */}
            <div className="grid grid-4" style={{ marginBottom: '2rem' }}>
                <div className="stat-card">
                    <div className="stat-value">{current_dataset.total_equipment}</div>
                    <div className="stat-label">Total Equipment</div>
                </div>
                <div className="stat-card">
                    <div className="stat-value stat-healthy">{current_dataset.healthy_count}</div>
                    <div className="stat-label">Healthy</div>
                </div>
                <div className="stat-card">
                    <div className="stat-value stat-warning">{current_dataset.warning_count}</div>
                    <div className="stat-label">Warning</div>
                </div>
                <div className="stat-card">
                    <div className="stat-value stat-critical">{current_dataset.critical_count}</div>
                    <div className="stat-label">Critical</div>
                </div>
            </div>

            {/* Parameter Averages */}
            <div className="grid grid-3" style={{ marginBottom: '2rem' }}>
                <div className="stat-card">
                    <div className="stat-value" style={{ color: 'var(--accent-primary)' }}>
                        {parameter_trends.avg_flowrate.toFixed(2)}
                    </div>
                    <div className="stat-label">Avg Flowrate</div>
                </div>
                <div className="stat-card">
                    <div className="stat-value" style={{ color: 'var(--accent-primary)' }}>
                        {parameter_trends.avg_pressure.toFixed(2)}
                    </div>
                    <div className="stat-label">Avg Pressure</div>
                </div>
                <div className="stat-card">
                    <div className="stat-value" style={{ color: 'var(--accent-primary)' }}>
                        {parameter_trends.avg_temperature.toFixed(2)}°C
                    </div>
                    <div className="stat-label">Avg Temperature</div>
                </div>
            </div>

            {/* Charts */}
            <h2 style={{ marginBottom: '1rem', marginTop: '2rem' }}>Visualizations</h2>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
                <div className="card">
                    <EquipmentTypeChart data={current_dataset.type_distribution} />
                </div>
                <div className="card">
                    <RiskDistributionChart data={risk_distribution} />
                </div>
            </div>



            {/* Trend Comparison */}
            {trend_comparison && (
                <>
                    <h2 style={{ marginBottom: '1rem' }}>Trend Comparison</h2>
                    <div className="card" style={{ marginBottom: '2rem' }}>
                        <div style={{ padding: '1rem' }}>
                            <p><strong>Pressure Change:</strong> {trend_comparison.pressure_change}%</p>
                            <p><strong>Temperature Change:</strong> {trend_comparison.temperature_change}%</p>
                            <p><strong>Flowrate Change:</strong> {trend_comparison.flowrate_change}%</p>
                        </div>

                        {trend_comparison.new_critical_equipment && trend_comparison.new_critical_equipment.length > 0 && (
                            <div className="alert alert-warning" style={{ marginTop: '1rem' }}>
                                <strong>New Critical Equipment:</strong> {trend_comparison.new_critical_equipment.join(', ')}
                            </div>
                        )}
                    </div>
                </>
            )}

            {/* Critical Equipment */}
            {critical_equipment.length > 0 && (
                <div className="card">
                    <h3 className="card-header">🚨 Critical Equipment</h3>
                    <div className="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>Equipment Name</th>
                                    <th>Type</th>
                                    <th>Health Score</th>
                                    <th>Risk Level</th>
                                    <th>Anomaly</th>
                                    <th>Recommendations</th>
                                </tr>
                            </thead>
                            <tbody>
                                {critical_equipment.map((eq) => (
                                    <tr key={eq.id}>
                                        <td><strong>{eq.name}</strong></td>
                                        <td>{eq.equipment_type}</td>
                                        <td>{eq.health_score.toFixed(1)}</td>
                                        <td>
                                            <span className={`badge badge-${eq.risk_level.toLowerCase()}`}>
                                                {eq.risk_level}
                                            </span>
                                        </td>
                                        <td>
                                            {eq.is_anomaly && (
                                                <span className="badge badge-critical" title={eq.anomaly_reasons?.join(', ')}>
                                                    ⚠️ Anomaly
                                                </span>
                                            )}
                                        </td>
                                        <td style={{ fontSize: '0.85rem' }}>{eq.recommendations}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}
        </div>
    );
}

export default Dashboard;
