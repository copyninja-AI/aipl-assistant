# Fantasy Cricket Auction AI System

## Project Overview
End-to-end fantasy cricket auction system with AI-powered bidding assistance, player analytics, and auction simulation capabilities.

## System Architecture

### Architecture Layers
1. **Presentation Layer** - Streamlit Frontend
2. **Validation Layer** - Input validation and sanitization
3. **Business Logic Layer** - Core business rules and workflows
4. **Algorithm Layer** - ML models, scoring engine, optimization
5. **Data Access Layer** - CSV-based data persistence
6. **Configuration Layer** - System configuration and constants

### Key Features
- Fantasy Points Scoring Engine
- Player Performance Analytics Dashboard
- ML-based Expected Points Prediction
- Auction Simulator (N-team simulation)
- Live AI Auction Bidding Assistant
- CRM for Auction Management
- Dark Horse Player Identification
- Interactive Team Builder

## Project Structure
```
fantasy-auction-ai-cline/
├── src/
│   ├── config/              # Configuration layer
│   ├── data_access/         # Data persistence layer
│   ├── validation/          # Input validation layer
│   ├── business_logic/      # Business rules and workflows
│   ├── algorithms/          # ML models and algorithms
│   ├── scoring/             # Fantasy points scoring engine
│   └── utils/               # Utility functions
├── frontend/                # Streamlit UI
├── data/
│   ├── raw/                 # Raw JSON data
│   ├── processed/           # Processed data
│   └── database/            # CSV database files
├── models/                  # Trained ML models
├── tests/                   # Unit tests
└── docs/                    # Documentation

```

## Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Run Application
```bash
streamlit run frontend/app.py
```

## Data Flow

1. **Data Ingestion**: Ball-by-ball JSON → Processed CSV
2. **Feature Engineering**: Player statistics and metrics
3. **Scoring Engine**: Calculate fantasy points
4. **ML Models**: Predict expected fantasy points
5. **Auction Simulation**: Multi-team auction scenarios
6. **Live Assistant**: Real-time bidding recommendations

## Technology Stack
- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **ML**: scikit-learn, XGBoost, Prophet
- **Data**: Pandas, NumPy
- **Storage**: CSV files (local filesystem)

## Configuration
- Number of teams: 2-30 (default: 10)
- Budget per team: 100 Cr
- Squad constraints based on team count (see Rules sheet)

## Development Timeline
Estimated: 5-6 hours for MVP with all core features
