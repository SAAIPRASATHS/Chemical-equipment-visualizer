# Chemical Equipment Health Intelligence & Predictive Monitoring System

A full-stack hybrid application that analyzes CSV data of chemical equipment and provides health scoring, risk classification, predictive insights, and visualization dashboards through both **Web (React.js)** and **Desktop (PyQt5)** interfaces.

![Project Banner](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![React](https://img.shields.io/badge/React-18.2-61dafb)
![Django](https://img.shields.io/badge/Django-4.2-green)

## 🎯 Features

### Core Functionality
- ✅ **JWT-based Authentication** - Secure role-based access (Admin, Viewer)
- ✅ **CSV Upload & Validation** - Automatic structure validation and error handling
- ✅ **Health Score Calculation** - Advanced algorithm considering pressure, temperature, and flowrate
- ✅ **Risk Classification** - Automatic categorization (Healthy, Warning, Critical)
- ✅ **Smart Recommendations** - Context-aware maintenance suggestions
- ✅ **Trend Comparison** - Compare current vs. previous datasets
- ✅ **History Management** - Store and compare last 5 datasets
- ✅ **PDF Report Generation** - Professional reports with embedded charts
- ✅ **Executive Auto-Summary** - Natural language insights

### Visualizations
- 📊 **Equipment Type Distribution** (Bar Chart)
- 🥧 **Risk Distribution** (Pie Chart)
- 📈 **Parameter Trends** (Line Chart)
- 📋 **Critical Equipment Table**
- 📉 **Summary Statistics Cards**

## 🏗️ Tech Stack

### Backend
- **Python** - Core language
- **Django 4.2** - Web framework
- **Django REST Framework** - API development
- **Pandas** - Data analysis
- **SQLite** - Database
- **JWT** - Authentication
- **ReportLab** - PDF generation

### Web Frontend
- **React.js 18** - UI framework
- **Vite** - Build tool
- **Axios** - HTTP client
- **Chart.js** - Data visualization
- **React Router** - Navigation

### Desktop Frontend
- **PyQt5** - GUI framework
- **Matplotlib** - Charts and graphs
- **QTableWidget** - Data tables

## 📁 Project Structure

```
chemical-equipment-intelligence/
├── backend/
│   ├── backend/
│   │   ├── settings.py          # Django configuration
│   │   ├── urls.py               # URL routing
│   │   ├── wsgi.py               # WSGI config
│   │   └── asgi.py               # ASGI config
│   ├── api/
│   │   ├── models.py             # Database models
│   │   ├── views.py              # API endpoints
│   │   ├── serializers.py        # DRF serializers
│   │   ├── analysis.py           # Health scoring engine
│   │   ├── report_generator.py   # PDF generation
│   │   ├── urls.py               # API routes
│   │   └── admin.py              # Admin interface
│   ├── manage.py                 # Django management
│   ├── requirements.txt          # Python dependencies
│   ├── .env                      # Environment variables
│   └── sample_data.csv           # Test data
├── web-frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Login.jsx         # Authentication UI
│   │   │   ├── Dashboard.jsx     # Main dashboard
│   │   │   ├── Upload.jsx        # CSV upload
│   │   │   ├── History.jsx       # Dataset history
│   │   │   └── Charts.jsx        # Chart components
│   │   ├── services/
│   │   │   └── api.js            # API client
│   │   ├── App.jsx               # Main component
│   │   ├── App.css               # Styles
│   │   └── main.jsx              # Entry point
│   ├── package.json              # Dependencies
│   ├── vite.config.js            # Vite config
│   └── index.html                # HTML template
├── desktop-frontend/
│   ├── ui/
│   │   ├── login_dialog.py       # Login UI
│   │   ├── main_window.py        # Main window
│   │   ├── dashboard_widget.py   # Dashboard
│   │   └── upload_widget.py      # Upload UI
│   ├── services/
│   │   └── api_client.py         # API client
│   ├── main.py                   # Entry point
│   └── requirements.txt          # Dependencies
└── README.md                     # This file
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

### 2. Web Frontend Setup

```bash
# Navigate to web frontend directory
cd web-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The web app will be available at `http://localhost:3000`

### 3. Desktop Frontend Setup

```bash
# Navigate to desktop frontend directory
cd desktop-frontend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

## 📊 Health Score Algorithm

The health score is calculated using the following formula:

```
Health Score = 100 
             - (Pressure / MaxSafePressure × 30)
             - (Temperature / MaxSafeTemperature × 40)
             + Flowrate Stability Bonus
```

**Risk Classification:**
- **80-100**: Healthy ✅
- **50-79**: Warning ⚠️
- **0-49**: Critical 🚨

**Default Safety Limits:**
- Max Safe Pressure: 100 bar
- Max Safe Temperature: 200°C

## 📝 CSV Format

Your CSV file must include these columns:

| Column Name      | Type    | Description                    |
|------------------|---------|--------------------------------|
| Equipment Name   | Text    | Unique equipment identifier    |
| Type             | Text    | Equipment type (e.g., Pump)    |
| Flowrate         | Number  | Flow rate measurement          |
| Pressure         | Number  | Pressure measurement           |
| Temperature      | Number  | Temperature in °C              |

**Example CSV:**
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor-A1,Reactor,45.5,85.2,175.3
Pump-B2,Pump,32.1,65.4,95.2
Valve-C3,Valve,28.7,92.8,110.5
```

## 🔐 API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT tokens
- `POST /api/token/refresh/` - Refresh access token
- `POST /api/register/` - Register new user

### Data Management
- `POST /api/upload/` - Upload CSV file
- `GET /api/summary/` - Get current dataset summary
- `GET /api/history/` - Get upload history
- `GET /api/dataset/<id>/` - Get dataset details
- `GET /api/report/<id>/` - Download PDF report

## 🎨 Features Showcase

### Smart Recommendations
The system provides context-aware recommendations:
- **High Pressure** → Valve inspection recommended
- **High Temperature** → Cooling system check
- **Low Flowrate** → Pump calibration needed

### Trend Analysis
Compare consecutive datasets to identify:
- Percentage changes in pressure, temperature, flowrate
- New critical equipment
- Performance degradation patterns

### Executive Summary
Auto-generated natural language summaries:
> "Out of 120 equipment units analyzed, 15% are in critical condition. Valve systems show highest pressure-related risk. Immediate inspection is recommended."

## 🎯 Usage Guide

### Web Application
1. **Login** - Use your credentials or register
2. **Upload CSV** - Navigate to Upload tab and select your file
3. **View Dashboard** - Analyze health scores and visualizations
4. **Download Report** - Generate PDF reports for documentation
5. **Check History** - Compare with previous uploads

### Desktop Application
1. **Launch** - Run `python main.py`
2. **Login** - Enter credentials in the dialog
3. **Dashboard Tab** - View real-time analytics
4. **Upload Tab** - Select and upload CSV files
5. **Download Reports** - Save PDF reports locally

## 🛠️ Configuration

Edit `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Health score parameters
MAX_SAFE_PRESSURE=100
MAX_SAFE_TEMPERATURE=200

# JWT settings
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440
```

## 🧪 Testing

### Test with Sample Data
A sample CSV file is provided at `backend/sample_data.csv`

### Create Test User
```bash
python manage.py createsuperuser
```

### Access Admin Panel
Visit `http://localhost:8000/admin` to manage data

## 🐛 Troubleshooting

### Backend Issues
- **Port 8000 in use**: Change port in `manage.py runserver 8001`
- **Database errors**: Delete `db.sqlite3` and re-run migrations
- **Import errors**: Ensure virtual environment is activated

### Frontend Issues
- **npm install fails**: Clear cache with `npm cache clean --force`
- **Port 3000 in use**: Vite will automatically use next available port
- **API connection**: Check backend is running on port 8000

### Desktop Issues
- **PyQt5 import error**: Reinstall with `pip install PyQt5==5.15.10`
- **Matplotlib errors**: Install with `pip install matplotlib==3.8.2`

## 📦 Production Deployment

### Backend
```bash
# Set DEBUG=False in .env
# Use PostgreSQL instead of SQLite
# Configure ALLOWED_HOSTS
# Collect static files
python manage.py collectstatic
```

### Web Frontend
```bash
npm run build
# Deploy dist/ folder to hosting service
```

## 🤝 Contributing

This is a demonstration project. For production use:
1. Implement comprehensive testing
2. Add input sanitization
3. Use PostgreSQL for production
4. Implement rate limiting
5. Add logging and monitoring

## 📄 License

This project is created for educational and demonstration purposes.

## 👨‍💻 Author

Built with ❤️ using Django, React, and PyQt5

---

**Note**: This system is designed as a lightweight industrial predictive maintenance platform. Always validate results with domain experts before making critical decisions.
