# Grazescale Weight Estimation

A Python-based application for estimating livestock weight using morphometric measurements with a modern web interface.

## Overview

Grazescale Weight Estimation is a tool designed to help farmers and livestock professionals estimate the weight of animals using morphometric measurements. This non-invasive method provides a convenient alternative to traditional weighing methods.

## Live Demo

Visit our application at: [Grazescale Weight Estimation](https://grazescale-weight-estimation.vercel.app/)

## Features

- Morphometric measurement processing
- Livestock weight estimation
- RESTful API interface
- Interactive web interface
- Real-time weight calculations
- Data visualization and reporting
- Mobile-responsive design

## Project Structure

```
├── backend/            # Backend Application
│   ├── app/
│   │   ├── main.py          # Application entry point
│   │   ├── routes.py        # API route definitions
│   │   ├── models/
│   │   │   └── livestock_measurement.py  # Data models
│   │   └── services/
│   │       ├── morphometric.py   # Morphometric calculation logic
│   │       └── utils.py          # Utility functions
│   └── requirements.txt    # Backend dependencies
├── grazescale-frontend/            # Frontend Application
│   ├── public/         # Static files
│   ├── src/
│   │   ├── components/
|   |   |      └── UploadForm.js # React components
│   │   └── App.js     # Root component
│   ├── package.json    # Frontend dependencies
│   └── README.md      # Frontend documentation
└── LICENSE            # License information
```

## Technology Stack

### Backend
- Python 3.x
- Flask (Web Framework)
- SQLAlchemy (ORM)
- NumPy (Numerical Computations)
- Pytest (Testing)

### Frontend
- React.js
- Material-UI
- Chart.js
- Axios
- Jest (Testing)

## Prerequisites

- Python 3.x
- pip (Python package installer)
- Node.js and npm

## Installation

1. Clone the repository:
```bash
git clone https://github.com/pranjaltile/Grazescale_weight_estimation.git
cd Grazescale_weight_estimation
```

2. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd frontend
npm install
```

## Running the Application

1. Start the backend server:
```bash
cd backend
python app/main.py
```

2. Start the frontend development server:
```bash
cd frontend
npm start
```

3. Access the application:
- Frontend: `https://grazescale-weight-estimation.vercel.app/`
- Backend API: `https://grazescale-backendapi.onrender.com/`

## API Endpoints

### Measurements
- `POST /api/estimate`: Submit morphometric measurements for weight estimation
- `GET /api/measurements`: Retrieve measurement history
- `GET /api/measurements/<id>`: Get specific measurement details
- `DELETE /api/measurements/<id>`: Delete a measurement record



## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the terms included in the [LICENSE](LICENSE) file.


