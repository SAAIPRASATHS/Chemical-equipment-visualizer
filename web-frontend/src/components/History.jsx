import React, { useState, useEffect } from 'react';
import { getHistory, getDatasetDetail, generateReport } from '../services/api';

function History() {
    const [history, setHistory] = useState([]);
    const [selectedDataset, setSelectedDataset] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        try {
            setLoading(true);
            const data = await getHistory();
            setHistory(data.datasets);
            setError('');
        } catch (err) {
            setError('Failed to load history');
        } finally {
            setLoading(false);
        }
    };

    const handleViewDetails = async (datasetId) => {
        try {
            const data = await getDatasetDetail(datasetId);
            setSelectedDataset(data);
        } catch (err) {
            alert('Failed to load dataset details');
        }
    };

    const handleDownloadReport = (datasetId) => {
        const reportUrl = generateReport(datasetId);
        window.open(reportUrl, '_blank');
    };

    if (loading) {
        return (
            <div className="loading">
                <div className="spinner"></div>
            </div>
        );
    }

    return (
        <div className="container">
            <h1 style={{ marginBottom: '2rem' }}>Upload History</h1>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
                View and compare your last 5 uploaded datasets
            </p>

            {error && <div className="alert alert-error">{error}</div>}

            {history.length === 0 ? (
                <div className="alert alert-warning">
                    No upload history found. Upload a CSV file to get started.
                </div>
            ) : (
                <div className="grid grid-2">
                    {history.map((dataset) => (
                        <div key={dataset.id} className="card">
                            <h3 className="card-header">{dataset.filename}</h3>

                            <div style={{ marginBottom: '1rem' }}>
                                <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                                    Uploaded: {new Date(dataset.upload_date).toLocaleString()}
                                </p>
                            </div>

                            <div className="grid grid-3" style={{ marginBottom: '1rem' }}>
                                <div>
                                    <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--accent-success)' }}>
                                        {dataset.healthy_count}
                                    </div>
                                    <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Healthy</div>
                                </div>
                                <div>
                                    <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--accent-warning)' }}>
                                        {dataset.warning_count}
                                    </div>
                                    <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Warning</div>
                                </div>
                                <div>
                                    <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--accent-danger)' }}>
                                        {dataset.critical_count}
                                    </div>
                                    <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Critical</div>
                                </div>
                            </div>

                            <div style={{ display: 'flex', gap: '0.5rem' }}>
                                <button
                                    onClick={() => handleViewDetails(dataset.id)}
                                    className="btn btn-secondary"
                                    style={{ flex: 1 }}
                                >
                                    View Details
                                </button>
                                <button
                                    onClick={() => handleDownloadReport(dataset.id)}
                                    className="btn btn-primary"
                                    style={{ flex: 1 }}
                                >
                                    Download Report
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* Dataset Details Modal */}
            {selectedDataset && (
                <div
                    style={{
                        position: 'fixed',
                        top: 0,
                        left: 0,
                        right: 0,
                        bottom: 0,
                        background: 'rgba(0, 0, 0, 0.8)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        zIndex: 1000,
                        padding: '2rem',
                        overflow: 'auto'
                    }}
                    onClick={() => setSelectedDataset(null)}
                >
                    <div
                        className="card"
                        style={{ maxWidth: '900px', width: '100%', maxHeight: '90vh', overflow: 'auto' }}
                        onClick={(e) => e.stopPropagation()}
                    >
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                            <h3 className="card-header" style={{ marginBottom: 0 }}>{selectedDataset.filename}</h3>
                            <button onClick={() => setSelectedDataset(null)} className="btn btn-secondary">
                                ✕ Close
                            </button>
                        </div>

                        <div className="alert alert-success" style={{ marginBottom: '1rem' }}>
                            {selectedDataset.executive_summary}
                        </div>

                        <div className="table-container">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Equipment Name</th>
                                        <th>Type</th>
                                        <th>Flowrate</th>
                                        <th>Pressure</th>
                                        <th>Temperature</th>
                                        <th>Health Score</th>
                                        <th>Risk</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {selectedDataset.equipment?.map((eq) => (
                                        <tr key={eq.id}>
                                            <td>{eq.name}</td>
                                            <td>{eq.equipment_type}</td>
                                            <td>{eq.flowrate.toFixed(2)}</td>
                                            <td>{eq.pressure.toFixed(2)}</td>
                                            <td>{eq.temperature.toFixed(2)}°C</td>
                                            <td>{eq.health_score.toFixed(1)}</td>
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
                </div>
            )}
        </div>
    );
}

export default History;
