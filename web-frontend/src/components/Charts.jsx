import React from 'react';
import { Bar, Pie, Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement,
    PointElement,
    LineElement,
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement,
    PointElement,
    LineElement
);

export function EquipmentTypeChart({ typeDistribution }) {
    const data = {
        labels: Object.keys(typeDistribution),
        datasets: [
            {
                label: 'Equipment Count',
                data: Object.values(typeDistribution),
                backgroundColor: [
                    'rgba(63, 81, 181, 0.8)',
                    'rgba(92, 107, 192, 0.8)',
                    'rgba(121, 134, 203, 0.8)',
                    'rgba(159, 168, 218, 0.8)',
                    'rgba(197, 202, 233, 0.8)',
                ],
                borderColor: 'rgba(63, 81, 181, 1)',
                borderWidth: 2,
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false,
            },
            title: {
                display: true,
                text: 'Equipment Type Distribution',
                color: '#e8eaf6',
                font: { size: 16, weight: 'bold' },
            },
        },
        scales: {
            y: {
                ticks: { color: '#9fa8da' },
                grid: { color: 'rgba(63, 81, 181, 0.2)' },
            },
            x: {
                ticks: { color: '#9fa8da' },
                grid: { color: 'rgba(63, 81, 181, 0.2)' },
            },
        },
    };

    return (
        <div style={{ height: '300px' }}>
            <Bar data={data} options={options} />
        </div>
    );
}

export function RiskDistributionChart({ riskDistribution }) {
    const data = {
        labels: ['Healthy', 'Warning', 'Critical'],
        datasets: [
            {
                data: [
                    riskDistribution.Healthy || 0,
                    riskDistribution.Warning || 0,
                    riskDistribution.Critical || 0,
                ],
                backgroundColor: [
                    'rgba(76, 175, 80, 0.8)',
                    'rgba(255, 152, 0, 0.8)',
                    'rgba(244, 67, 54, 0.8)',
                ],
                borderColor: ['#4caf50', '#ff9800', '#f44336'],
                borderWidth: 2,
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: { color: '#e8eaf6' },
            },
            title: {
                display: true,
                text: 'Risk Distribution',
                color: '#e8eaf6',
                font: { size: 16, weight: 'bold' },
            },
        },
    };

    return (
        <div style={{ height: '300px' }}>
            <Pie data={data} options={options} />
        </div>
    );
}

export function ParameterTrendsChart({ trendComparison }) {
    if (!trendComparison) return null;

    const data = {
        labels: ['Pressure', 'Temperature', 'Flowrate'],
        datasets: [
            {
                label: 'Change (%)',
                data: [
                    trendComparison.pressure_change,
                    trendComparison.temperature_change,
                    trendComparison.flowrate_change,
                ],
                backgroundColor: 'rgba(63, 81, 181, 0.2)',
                borderColor: 'rgba(63, 81, 181, 1)',
                borderWidth: 2,
                fill: true,
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false,
            },
            title: {
                display: true,
                text: 'Parameter Trends (% Change)',
                color: '#e8eaf6',
                font: { size: 16, weight: 'bold' },
            },
        },
        scales: {
            y: {
                ticks: { color: '#9fa8da' },
                grid: { color: 'rgba(63, 81, 181, 0.2)' },
            },
            x: {
                ticks: { color: '#9fa8da' },
                grid: { color: 'rgba(63, 81, 181, 0.2)' },
            },
        },
    };

    return (
        <div style={{ height: '300px' }}>
            <Line data={data} options={options} />
        </div>
    );
}
