import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login, register } from '../services/api';

function Login({ setIsAuthenticated }) {
    const [isLogin, setIsLogin] = useState(true);
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        role: 'viewer'
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            if (isLogin) {
                const data = await login(formData.username, formData.password);
                localStorage.setItem('access_token', data.access);
                localStorage.setItem('refresh_token', data.refresh);
                setIsAuthenticated(true);
                navigate('/upload');
            } else {
                await register(formData.username, formData.email, formData.password, formData.role);
                setError('');
                alert('Registration successful! Please login.');
                setIsLogin(true);
                // Reset form
                setFormData({
                    username: '',
                    email: '',
                    password: '',
                    role: 'viewer'
                });
            }
        } catch (err) {
            // Handle different error formats
            let errorMessage = 'Authentication failed. Please try again.';

            if (err.response?.data) {
                const errorData = err.response.data;

                // Check for detail message (login errors)
                if (errorData.detail) {
                    errorMessage = errorData.detail;
                }
                // Check for field-specific errors (registration errors)
                else if (typeof errorData === 'object') {
                    const errors = [];
                    for (const [field, messages] of Object.entries(errorData)) {
                        if (Array.isArray(messages)) {
                            errors.push(`${field}: ${messages.join(', ')}`);
                        } else {
                            errors.push(`${field}: ${messages}`);
                        }
                    }
                    if (errors.length > 0) {
                        errorMessage = errors.join('. ');
                    }
                }
            }

            setError(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    return (
        <div style={{
            minHeight: '100vh',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '2rem'
        }}>
            <div className="card" style={{ maxWidth: '450px', margin: '2rem auto' }}>
                <h1 style={{ textAlign: 'center', marginBottom: '2rem', color: 'var(--accent-primary)' }}>
                    Chemical Equipment Intelligence
                </h1>
                <div style={{
                    display: 'flex',
                    gap: '1rem',
                    marginBottom: '2rem',
                    borderBottom: '2px solid var(--border-color)'
                }}>
                    <button
                        className={`btn ${isLogin ? 'btn-primary' : 'btn-secondary'}`}
                        onClick={() => setIsLogin(true)}
                        style={{ flex: 1, borderRadius: '8px 8px 0 0' }}
                    >
                        Login
                    </button>
                    <button
                        className={`btn ${!isLogin ? 'btn-primary' : 'btn-secondary'}`}
                        onClick={() => setIsLogin(false)}
                        style={{ flex: 1, borderRadius: '8px 8px 0 0' }}
                    >
                        Register
                    </button>
                </div>

                {error && (
                    <div className="alert alert-error">{error}</div>
                )}

                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label className="form-label">Username</label>
                        <input
                            type="text"
                            name="username"
                            className="form-input"
                            value={formData.username}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    {!isLogin && (
                        <div className="form-group">
                            <label className="form-label">Email</label>
                            <input
                                type="email"
                                name="email"
                                className="form-input"
                                value={formData.email}
                                onChange={handleChange}
                                required
                            />
                        </div>
                    )}

                    <div className="form-group">
                        <label className="form-label">Password</label>
                        <input
                            type="password"
                            name="password"
                            className="form-input"
                            value={formData.password}
                            onChange={handleChange}
                            required
                            minLength={8}
                        />
                    </div>

                    {!isLogin && (
                        <div className="form-group">
                            <label className="form-label">Role</label>
                            <select
                                name="role"
                                className="form-input"
                                value={formData.role}
                                onChange={handleChange}
                            >
                                <option value="viewer">Viewer</option>
                                <option value="admin">Admin</option>
                            </select>
                        </div>
                    )}

                    <button
                        type="submit"
                        className="btn btn-primary"
                        style={{ width: '100%' }}
                        disabled={loading}
                    >
                        {loading ? 'Processing...' : (isLogin ? 'Login' : 'Register')}
                    </button>
                </form>
            </div>
        </div>
    );
}

export default Login;
