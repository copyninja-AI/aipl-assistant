# Fantasy Cricket Auction AI - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Initialize Data
This will process all match data and prepare the system:
```bash
python initialize_data.py
```

**What this does:**
- Processes 100+ IPL match JSON files
- Calculates fantasy points for all players
- Generates player statistics and aggregates
- Loads auction players from PLAYERS_RULES.xlsx
- Initializes the CSV database

**Expected time:** 2-3 minutes

### Step 3: Launch the Application
```bash
streamlit run frontend/app.py
```

The application will open in your browser at `http://localhost:8501`

---

## 📋 System Workflow

### 1. **Setup Phase** (CRM - Setup)
1. Navigate to **⚙️ CRM - Setup**
2. Go to **Teams Management** tab
3. Create teams (e.g., Team1, Team2, ... Team10)
4. Configure number of teams in **Configuration** tab

### 2. **Pre-Auction Analysis** (Player Analytics)
1. Navigate to **📊 Player Analytics**
2. Explore:
   - **Top Performers**: Best players by fantasy points
   - **Value Analysis**: Price vs Performance scatter plot
   - **Dark Horses**: Undervalued players with high potential

### 3. **Strategy Planning** (Predictions & Team Builder)
1. **🔮 Predictions**: View expected fantasy points for all players
2. **👥 Team Builder**: Build and test different team combinations

### 4. **Live Auction** (Auction Assistant & Live Auction)
1. **🎯 Auction Assistant**: 
   - Select your team
   - Enter player on auction
   - Get AI-powered bidding recommendations
   
2. **⚙️ CRM - Auction Data Entry**:
   - Record each sale (player, team, price)
   - System automatically updates:
     - Team purse
     - Squad composition
     - Player status

3. **📈 Live Auction**:
   - Monitor all teams' progress
   - Track auction completion
   - View real-time standings

---

## 🎯 Key Features

### Fantasy Points Engine
- **Ball-by-ball analysis** of historical IPL data
- **Comprehensive scoring** including:
  - Batting: Runs, 4s, 6s, Strike Rate bonuses
  - Bowling: Wickets, Maidens, Dots, Economy bonuses
  - Fielding: Catches, Stumpings, Runouts
  - Bonuses: Starting XI, Impact Player, Winning Team, MOTM

### Player Analytics
- **Performance Metrics**: Points per match, consistency scores
- **Value Scores**: Expected points / Auction price
- **Category Analysis**: BAT, BOWL, AR, WK breakdowns
- **Dark Horse Identification**: High-value, low-price players

### AI Auction Assistant
- **Real-time Recommendations**: BID or PASS decisions
- **Max Bid Calculations**: Based on:
  - Expected fantasy points
  - Team purse remaining
  - Squad balance needs
- **Constraint Checking**: Overseas limits, category limits

### CRM System
- **Team Management**: Create, update, delete teams
- **Auction Tracking**: Record all bids and sales
- **Squad Monitoring**: Real-time purse and composition tracking
- **Transaction History**: Complete audit trail

---

## 📊 Data Files

### Input Files
- `PLAYERS_RULES.xlsx`: Player list and auction rules
- `data/raw/ipl_male_json/*.json`: Ball-by-ball match data

### Generated Files (after initialization)
- `data/processed/all_fantasy_points.csv`: Fantasy points per match
- `data/processed/player_aggregates.csv`: Aggregated statistics
- `data/processed/auction_players.csv`: Players in auction
- `data/processed/players_with_stats.csv`: Merged player data
- `data/processed/feature_matrix.csv`: ML features

### Database Files (CSV)
- `data/database/teams.csv`: Team information
- `data/database/players.csv`: Player master data
- `data/database/auction_bids.csv`: All bids
- `data/database/team_squads.csv`: Team compositions
- `data/database/fantasy_points.csv`: Historical fantasy points
- `data/database/predictions.csv`: ML predictions

---

## 🎮 Usage Scenarios

### Scenario 1: Pre-Auction Preparation
```
1. Run initialize_data.py
2. Open Player Analytics
3. Identify top performers in each category
4. Note dark horse players
5. Create target player list
```

### Scenario 2: Live Auction
```
1. Create all teams in CRM
2. For each player:
   a. Open Auction Assistant
   b. Select your team
   c. Enter player on auction
   d. Get recommendation
   e. Make decision
   f. Record sale in CRM
3. Monitor progress in Live Auction dashboard
```

### Scenario 3: Team Building
```
1. Open Team Builder
2. Set budget and squad size
3. Select players
4. Check:
   - Total cost vs budget
   - Squad composition
   - Expected points
5. Adjust until optimal
```

---

## 🔧 Troubleshooting

### Issue: "No players loaded"
**Solution**: Run `python initialize_data.py` first

### Issue: "Player statistics not found"
**Solution**: Ensure `data/processed/players_with_stats.csv` exists after initialization

### Issue: Import errors
**Solution**: Install all dependencies: `pip install -r requirements.txt`

### Issue: Slow data processing
**Solution**: Normal for first run (100+ matches). Subsequent runs use cached data.

---

## 📈 Performance Metrics

### Data Processing
- **Matches Processed**: 100+ IPL matches
- **Players Analyzed**: 400+ players
- **Fantasy Points Calculated**: 2000+ player-match records

### System Capabilities
- **Teams Supported**: 2-30 teams
- **Concurrent Users**: Multi-user support via CSV database
- **Real-time Updates**: Instant dashboard refresh

---

## 🎯 Winning Strategy Tips

### 1. **Value Hunting**
- Focus on players with high value scores (points/price ratio)
- Target dark horses in accelerated auction

### 2. **Squad Balance**
- Maintain category constraints
- Don't overspend early
- Keep purse for final rounds

### 3. **Data-Driven Decisions**
- Use AI recommendations
- Check historical fantasy points
- Consider recent form (if available)

### 4. **Constraint Management**
- Track overseas count
- Monitor category distribution
- Plan for minimum requirements

---

## 📞 Support

For issues or questions:
1. Check this guide
2. Review README.md
3. Check data/processed/ for generated files
4. Verify database initialization

---

## 🎉 Ready to Win!

You now have a complete AI-powered auction system. Use the analytics, follow the AI recommendations, and may the best team win! 🏆

**Remember**: The goal is to maximize fantasy points within budget and constraints. Good luck! 🍀
