import React, { useState } from 'react';
import { uploadCSV } from '../services/api';

function Upload({ onUploadSuccess }) {
    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile && selectedFile.name.endsWith('.csv')) {
            setFile(selectedFile);
            setError('');
        } else {
            setError('Please select a valid CSV file');
            setFile(null);
        }
    };

    const handleUpload = async (e) => {
        e.preventDefault();
        if (!file) {
            setError('Please select a file');
            return;
        }

        setUploading(true);
        setError('');
        setSuccess('');

        try {
            const response = await uploadCSV(file);
            setSuccess('CSV uploaded and analyzed successfully!');
            setFile(null);
            e.target.reset();

            if (onUploadSuccess) {
                onUploadSuccess();
            }
        } catch (err) {
            setError(err.response?.data?.error || 'Upload failed. Please check your CSV format.');
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="container">
            <h1 style={{ marginBottom: '2rem' }}>Upload Equipment Data</h1>

            <div className="card" style={{ marginBottom: '2rem' }}>
                <h2 style={{ marginBottom: '1rem' }}>CSV Format Requirements</h2>
                <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>
                    Upload a CSV file with the following columns:
                </p>
                <div className="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Column Name</th>
                                <th>Description</th>
                                <th>Type</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Equipment Name</td>
                                <td>Unique identifier for equipment</td>
                                <td>Text</td>
                            </tr>
                            <tr>
                                <td>Type</td>
                                <td>Equipment type (e.g., Pump, Valve)</td>
                                <td>Text</td>
                            </tr>
                            <tr>
                                <td>Flowrate</td>
                                <td>Flow rate measurement</td>
                                <td>Number</td>
                            </tr>
                            <tr>
                                <td>Pressure</td>
                                <td>Pressure measurement</td>
                                <td>Number</td>
                            </tr>
                            <tr>
                                <td>Temperature</td>
                                <td>Temperature measurement (°C)</td>
                                <td>Number</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            {error && <div className="alert alert-error">{error}</div>}
            {success && <div className="alert alert-success">{success}</div>}

            <form onSubmit={handleUpload}>
                <div className="form-group">
                    <label className="form-label">Select CSV File</label>
                    <input
                        type="file"
                        accept=".csv"
                        onChange={handleFileChange}
                        className="form-input"
                        disabled={uploading}
                    />
                </div>

                <button
                    onClick={handleUpload}
                    disabled={!file || uploading}
                    className="btn btn-success"
                    style={{ width: '100%', padding: '1rem', fontSize: '1.1rem' }}
                >
                    {uploading ? 'Uploading...' : 'Upload & Analyze'}
                </button>
            </form>
        </div>
    );
}

export default Upload;
