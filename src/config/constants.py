"""
Configuration Constants
Centralized configuration for the fantasy auction system
"""

from typing import Dict, List
from dataclasses import dataclass

# Auction Configuration
AUCTION_PURSE = 100  # in Crores
MIN_TEAMS = 2
MAX_TEAMS = 30
DEFAULT_TEAMS = 10

# Squad Constraints by Team Count
SQUAD_CONSTRAINTS = {
    7: {
        'total_players': 20,
        'bat': {'min': 4, 'max': 7},
        'bowl': {'min': 4, 'max': 7},
        'ar': {'min': 3, 'max': 7},
        'wk': {'min': 2, 'max': 5},
        'overseas': {'max': 10}
    },
    8: {
        'total_players': 18,
        'bat': {'min': 4, 'max': 7},
        'bowl': {'min': 4, 'max': 7},
        'ar': {'min': 3, 'max': 7},
        'wk': {'min': 2, 'max': 4},
        'overseas': {'max': 9}
    },
    9: {
        'total_players': 16,
        'bat': {'min': 3, 'max': 6},
        'bowl': {'min': 3, 'max': 6},
        'ar': {'min': 2, 'max': 6},
        'wk': {'min': 1, 'max': 4},
        'overseas': {'max': 8}
    },
    10: {
        'total_players': 14,
        'bat': {'min': 3, 'max': 5},
        'bowl': {'min': 3, 'max': 5},
        'ar': {'min': 2, 'max': 5},
        'wk': {'min': 1, 'max': 4},
        'overseas': {'max': 7}
    }
}

# Base Prices (in Crores)
BASE_PRICES = [0.25, 0.50, 1.0, 1.5, 2.0]

# Bid Increment Rules
BID_INCREMENT_RULES = {
    'below_5cr': 0.25,  # 25L increment below 5Cr
    'above_5cr': 0.50   # 50L increment above 5Cr
}

# Player Categories
PLAYER_CATEGORIES = ['BAT', 'BOWL', 'AR', 'WK']

# Fantasy Points Scoring Rules
@dataclass
class ScoringRules:
    """Fantasy points scoring configuration"""
    
    # Batting
    RUN: int = 1
    FOUR: int = 1
    SIX: int = 2
    DUCK: int = -10  # Excluding bowlers
    
    # Bowling
    WICKET: int = 30
    MAIDEN: int = 25
    DOT_BALL: int = 1
    LBW_BOWLED_BONUS: int = 10
    
    # Fielding
    CATCH: int = 10
    STUMPING: int = 20
    RUNOUT_DIRECT: int = 20
    RUNOUT_EACH: int = 10
    
    # Milestones - Batting
    RUNS_25: int = 10
    RUNS_50: int = 20
    RUNS_75: int = 30
    RUNS_100: int = 40
    RUNS_125: int = 50
    
    # Milestones - Bowling
    WICKETS_3: int = 20
    WICKETS_4: int = 30
    WICKETS_5: int = 40
    WICKETS_6: int = 50
    
    # Strike Rate Bonus (min 6 balls)
    SR_BONUS = {
        (0, 40): -25,
        (40.01, 80): -15,
        (80.01, 120): -10,
        (120.01, 140): 0,
        (140.01, 160): 10,
        (160.01, 180): 15,
        (180.01, 200): 20,
        (200.01, 250): 30,
        (250.01, float('inf')): 40
    }
    
    # Economy Rate Bonus (min 1 over)
    ECONOMY_BONUS = {
        (0, 1.99): 50,
        (2, 2.99): 40,
        (3, 3.99): 30,
        (4, 4.99): 20,
        (5, 5.99): 10,
        (6, 7.99): 0,
        (8, 9.99): -10,
        (10, 11.99): -20,
        (12, float('inf')): -30
    }
    
    # Other Bonuses
    STARTING_XI: int = 5
    IMPACT_PLAYER: int = 5
    WINNING_TEAM: int = 10
    MAN_OF_MATCH: int = 50
    
    # Multipliers
    CAPTAIN_MULTIPLIER: float = 2.0
    VICE_CAPTAIN_MULTIPLIER: float = 1.5


SCORING_RULES = ScoringRules()

# Database Configuration
DATABASE_PATH = "data/database"
RAW_DATA_PATH = "data/raw/ipl_male_json"
PROCESSED_DATA_PATH = "data/processed"

# CSV Table Names
TABLES = {
    'teams': 'teams.csv',
    'players': 'players.csv',
    'auction_bids': 'auction_bids.csv',
    'team_squads': 'team_squads.csv',
    'player_stats': 'player_stats.csv',
    'fantasy_points': 'fantasy_points.csv',
    'predictions': 'predictions.csv'
}

# Overseas Players (Sample - to be expanded)
OVERSEAS_PLAYERS = [
    'Josh Hazlewood', 'Trent Boult', 'Mitchell Starc', 'Kagiso Rabada',
    'Jos Buttler', 'Heinrich Klaasen', 'Nicholas Pooran', 'Travis Head',
    'Mitchell Marsh', 'Cameron Green', 'Sam Curran', 'Pat Cummins',
    'Rashid Khan', 'Sunil Narine', 'Glenn Phillips', 'Tim David',
    # Add more as needed
]

# Model Configuration
MODEL_CONFIG = {
    'random_forest': {
        'n_estimators': 100,
        'max_depth': 10,
        'random_state': 42
    },
    'xgboost': {
        'n_estimators': 100,
        'max_depth': 6,
        'learning_rate': 0.1,
        'random_state': 42
    },
    'prophet': {
        'seasonality_mode': 'multiplicative',
        'changepoint_prior_scale': 0.05
    }
}

# Feature Engineering Configuration
FEATURE_CONFIG = {
    'rolling_windows': [3, 5, 10],  # Last N matches
    'aggregations': ['mean', 'std', 'max', 'min', 'sum'],
    'venue_encoding': True,
    'opponent_encoding': True,
    'recent_form_weight': 0.6  # Weight for recent matches
}

# Auction Simulation Configuration
SIMULATION_CONFIG = {
    'num_simulations': 1000,
    'risk_profiles': ['conservative', 'balanced', 'aggressive'],
    'strategy_weights': {
        'value_for_money': 0.3,
        'expected_points': 0.4,
        'squad_balance': 0.3
    }
}

# UI Configuration
UI_CONFIG = {
    'page_title': 'Fantasy Cricket Auction AI',
    'page_icon': '🏏',
    'layout': 'wide',
    'theme': {
        'primaryColor': '#FF4B4B',
        'backgroundColor': '#0E1117',
        'secondaryBackgroundColor': '#262730',
        'textColor': '#FAFAFA'
    }
}
