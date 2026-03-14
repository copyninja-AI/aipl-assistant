# System Architecture & Data Flow

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                          │
│                    (Streamlit Frontend)                         │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐     │
│  │   Home   │   CRM    │ Analytics│ Assistant│  Builder │     │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘     │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                    VALIDATION LAYER                             │
│         (Input Validation & Sanitization)                       │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                  BUSINESS LOGIC LAYER                           │
│  ┌──────────────┬──────────────┬──────────────┐               │
│  │ Auction Logic│ Team Manager │ Bid Validator│               │
│  └──────────────┴──────────────┴──────────────┘               │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                    ALGORITHM LAYER                              │
│  ┌──────────────┬──────────────┬──────────────┐               │
│  │ Scoring      │ ML Models    │ Optimization │               │
│  │ Engine       │ (Predictions)│ Algorithms   │               │
│  └──────────────┴──────────────┴──────────────┘               │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                  DATA ACCESS LAYER                              │
│              (CSV Database Manager)                             │
│  ┌──────────────┬──────────────┬──────────────┐               │
│  │   Teams      │   Players    │   Bids       │               │
│  │   Squads     │   Stats      │   Points     │               │
│  └──────────────┴──────────────┴──────────────┘               │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                  CONFIGURATION LAYER                            │
│         (Constants, Rules, Settings)                            │
└─────────────────────────────────────────────────────────────────┘
```

## 📊 Data Flow Diagram

### 1. Data Initialization Flow

```
┌──────────────────┐
│ Raw JSON Files   │
│ (Ball-by-Ball)   │
└────────┬─────────┘
         │
         ↓
┌──────────────────────────┐
│  Data Processor          │
│  - Parse JSON            │
│  - Extract player stats  │
└────────┬─────────────────┘
         │
         ↓
┌──────────────────────────┐
│  Fantasy Points Engine   │
│  - Calculate points      │
│  - Apply scoring rules   │
└────────┬─────────────────┘
         │
         ↓
┌──────────────────────────┐
│  Aggregation             │
│  - Group by player       │
│  - Calculate metrics     │
└────────┬─────────────────┘
         │
         ↓
┌──────────────────────────┐
│  Excel Parser            │
│  - Load auction players  │
│  - Extract base prices   │
└────────┬─────────────────┘
         │
         ↓
┌──────────────────────────┐
│  Data Merger             │
│  - Combine stats         │
│  - Feature engineering   │
└────────┬─────────────────┘
         │
         ↓
┌──────────────────────────┐
│  CSV Database            │
│  - Save to tables        │
│  - Initialize schema     │
└──────────────────────────┘
```

### 2. Auction Flow

```
┌──────────────────┐
│  User Action     │
│  (Create Team)   │
└────────┬─────────┘
         │
         ↓
┌──────────────────────────┐
│  Validation Layer        │
│  - Check constraints     │
│  - Validate input        │
└────────┬─────────────────┘
         │
         ↓
┌──────────────────────────┐
│  Business Logic          │
│  - Apply rules           │
│  - Update state          │
└────────┬─────────────────┘
         │
         ↓
┌──────────────────────────┐
│  Data Access Layer       │
│  - Write to CSV          │
│  - Update tables         │
└────────┬─────────────────┘
         │
         ↓
┌──────────────────────────┐
│  UI Update               │
│  - Refresh dashboard     │
│  - Show confirmation     │
└──────────────────────────┘
```

### 3. AI Recommendation Flow

```
┌──────────────────┐
│  Player on       │
│  Auction         │
└────────┬─────────┘
         │
         ↓
┌──────────────────────────┐
│  Load Player Stats       │
│  - Historical points     │
│  - Value score           │
└────────┬─────────────────┘
         │
         ↓
┌──────────────────────────┐
│  Load Team State         │
│  - Purse remaining       │
│  - Squad composition     │
│  - Constraints           │
└────────┬─────────────────┘
         │
         ↓
┌──────────────────────────┐
│  AI Algorithm            │
│  - Calculate max bid     │
│  - Check constraints     │
│  - Assess value          │
└────────┬─────────────────┘
         │
         ↓
┌──────────────────────────┐
│  Recommendation          │
│  - BID / PASS            │
│  - Max bid amount        │
│  - Reasoning             │
└──────────────────────────┘
```

## 🗄️ Database Schema (CSV Tables)

### teams.csv
```
team_id | team_name | purse_remaining | players_count | bat_count | bowl_count | ar_count | wk_count | overseas_count
--------|-----------|-----------------|---------------|-----------|------------|----------|----------|----------------
1       | Team1     | 100.0           | 0             | 0         | 0          | 0        | 0        | 0
```

### players.csv
```
player_id | player_name      | category | base_price | is_overseas | set_number | auction_status
----------|------------------|----------|------------|-------------|------------|---------------
1         | Virat Kohli      | BAT      | 2.0        | False       | 2          | unsold
2         | Jasprit Bumrah   | BOWL     | 2.0        | False       | 1          | unsold
```

### auction_bids.csv
```
bid_id | player_id | team_id | bid_amount | timestamp           | is_final
-------|-----------|---------|------------|---------------------|----------
1      | 1         | 1       | 2.5        | 2026-03-13 20:00:00 | False
2      | 1         | 2       | 3.0        | 2026-03-13 20:00:15 | True
```

### team_squads.csv
```
squad_id | team_id | player_id | purchase_price
---------|---------|-----------|---------------
1        | 2       | 1         | 3.0
```

### fantasy_points.csv
```
point_id | player_name    | match_id | batting_points | bowling_points | fielding_points | bonus_points | total_points
---------|----------------|----------|----------------|----------------|-----------------|--------------|-------------
1        | Virat Kohli    | 1        | 45             | 0              | 10              | 15           | 70
```

### predictions.csv
```
prediction_id | player_name    | expected_points | confidence_low | confidence_high | model_used | prediction_date
--------------|----------------|-----------------|----------------|-----------------|------------|----------------
1             | Virat Kohli    | 65.5            | 52.4           | 78.6            | XGBoost    | 2026-03-13
```

## 🔄 Component Interactions

### Fantasy Points Engine
**Input**: Match JSON data
**Process**: 
- Parse ball-by-ball data
- Calculate batting/bowling/fielding points
- Apply bonuses and multipliers
**Output**: Player fantasy points DataFrame

### Data Processor
**Input**: Raw JSON files, Excel file
**Process**:
- Process all matches
- Generate aggregates
- Merge data sources
- Feature engineering
**Output**: Processed CSV files

### CSV Database
**Input**: CRUD operations
**Process**:
- Read/Write CSV files
- Maintain referential integrity
- Handle transactions
**Output**: Data persistence

### Streamlit Frontend
**Input**: User interactions
**Process**:
- Display dashboards
- Handle forms
- Visualize data
**Output**: Interactive UI

## 🎯 Key Design Patterns

### 1. Repository Pattern
- `CSVDatabase` class abstracts data access
- Clean separation from business logic
- Easy to swap storage backend

### 2. Strategy Pattern
- Different auction strategies
- Pluggable ML models
- Configurable scoring rules

### 3. Factory Pattern
- Create teams, players, bids
- Consistent object creation
- Validation at creation

### 4. Observer Pattern
- UI updates on data changes
- Real-time dashboard refresh
- Event-driven architecture

## 🔐 SOLID Principles Implementation

### Single Responsibility
- Each class has one clear purpose
- `FantasyPointsEngine`: Only calculates points
- `CSVDatabase`: Only handles data persistence
- `DataProcessor`: Only processes raw data

### Open/Closed
- Extensible through configuration
- New scoring rules via constants
- New ML models via plugins

### Liskov Substitution
- Database interface can be swapped
- Different storage backends possible

### Interface Segregation
- Focused interfaces for each layer
- No unnecessary dependencies

### Dependency Inversion
- Depend on abstractions
- Configuration-driven behavior
- Loose coupling between layers

## 📈 Performance Considerations

### Data Processing
- **Batch processing**: Process all matches at once
- **Caching**: Store processed data
- **Incremental updates**: Only process new data

### Database Operations
- **CSV format**: Fast read/write
- **Indexed lookups**: Use pandas efficiently
- **Minimal I/O**: Cache in memory when possible

### UI Responsiveness
- **Session state**: Maintain state across interactions
- **Lazy loading**: Load data on demand
- **Async operations**: Non-blocking UI updates

## 🔮 Future Enhancements

1. **ML Models**: Implement XGBoost, Random Forest, Prophet
2. **Auction Simulator**: Monte Carlo simulations
3. **Real-time Sync**: WebSocket for live updates
4. **Advanced Analytics**: Player comparison, trend analysis
5. **Export Features**: PDF reports, Excel exports
6. **Mobile App**: React Native frontend
7. **API Layer**: REST API for integrations
8. **Authentication**: Multi-user with roles

## 📊 System Metrics

- **Lines of Code**: ~3000+
- **Components**: 15+ modules
- **Database Tables**: 7 CSV tables
- **UI Pages**: 7 dashboards
- **Processing Speed**: 100+ matches in 2-3 minutes
- **Scalability**: Supports 2-30 teams
