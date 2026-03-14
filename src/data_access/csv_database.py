"""
CSV Database Manager
Handles all data persistence operations using CSV files
Implements Repository pattern for clean data access
"""

import os
import pandas as pd
from typing import Dict, List, Optional, Any
from pathlib import Path
from ..config.constants import DATABASE_PATH, TABLES


class CSVDatabase:
    """
    CSV-based database manager implementing Repository pattern
    Provides CRUD operations for all entities
    """
    
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = Path(db_path)
        self.db_path.mkdir(parents=True, exist_ok=True)
        self._initialize_tables()
    
    def _initialize_tables(self):
        """Initialize all CSV tables if they don't exist"""
        
        # Teams table
        teams_path = self.db_path / TABLES['teams']
        if not teams_path.exists():
            pd.DataFrame(columns=[
                'team_id', 'team_name', 'purse_remaining', 'players_count',
                'bat_count', 'bowl_count', 'ar_count', 'wk_count', 'overseas_count'
            ]).to_csv(teams_path, index=False)
        
        # Players table
        players_path = self.db_path / TABLES['players']
        if not players_path.exists():
            pd.DataFrame(columns=[
                'player_id', 'player_name', 'category', 'base_price',
                'is_overseas', 'set_number', 'auction_status'
            ]).to_csv(players_path, index=False)
        
        # Auction bids table
        bids_path = self.db_path / TABLES['auction_bids']
        if not bids_path.exists():
            pd.DataFrame(columns=[
                'bid_id', 'player_id', 'team_id', 'bid_amount', 'timestamp', 'is_final'
            ]).to_csv(bids_path, index=False)
        
        # Team squads table
        squads_path = self.db_path / TABLES['team_squads']
        if not squads_path.exists():
            pd.DataFrame(columns=[
                'squad_id', 'team_id', 'player_id', 'purchase_price'
            ]).to_csv(squads_path, index=False)
        
        # Player stats table
        stats_path = self.db_path / TABLES['player_stats']
        if not stats_path.exists():
            pd.DataFrame(columns=[
                'stat_id', 'player_name', 'match_id', 'runs', 'wickets',
                'catches', 'strike_rate', 'economy', 'total_matches'
            ]).to_csv(stats_path, index=False)
        
        # Fantasy points table
        points_path = self.db_path / TABLES['fantasy_points']
        if not points_path.exists():
            pd.DataFrame(columns=[
                'point_id', 'player_name', 'match_id', 'batting_points',
                'bowling_points', 'fielding_points', 'bonus_points', 'total_points'
            ]).to_csv(points_path, index=False)
        
        # Predictions table
        predictions_path = self.db_path / TABLES['predictions']
        if not predictions_path.exists():
            pd.DataFrame(columns=[
                'prediction_id', 'player_name', 'expected_points',
                'confidence_interval_low', 'confidence_interval_high',
                'model_used', 'prediction_date'
            ]).to_csv(predictions_path, index=False)
    
    # ==================== TEAMS OPERATIONS ====================
    
    def create_team(self, team_name: str, purse: float = 100.0) -> int:
        """Create a new team"""
        teams_df = self._read_table('teams')
        team_id = len(teams_df) + 1
        
        new_team = pd.DataFrame([{
            'team_id': team_id,
            'team_name': team_name,
            'purse_remaining': purse,
            'players_count': 0,
            'bat_count': 0,
            'bowl_count': 0,
            'ar_count': 0,
            'wk_count': 0,
            'overseas_count': 0
        }])
        
        teams_df = pd.concat([teams_df, new_team], ignore_index=True)
        self._write_table('teams', teams_df)
        return team_id
    
    def get_team(self, team_id: int) -> Optional[Dict]:
        """Get team by ID"""
        teams_df = self._read_table('teams')
        team = teams_df[teams_df['team_id'] == team_id]
        return team.to_dict('records')[0] if not team.empty else None
    
    def get_all_teams(self) -> pd.DataFrame:
        """Get all teams"""
        return self._read_table('teams')
    
    def update_team(self, team_id: int, updates: Dict):
        """Update team information"""
        teams_df = self._read_table('teams')
        for key, value in updates.items():
            teams_df.loc[teams_df['team_id'] == team_id, key] = value
        self._write_table('teams', teams_df)
    
    def delete_team(self, team_id: int):
        """Delete a team"""
        teams_df = self._read_table('teams')
        teams_df = teams_df[teams_df['team_id'] != team_id]
        self._write_table('teams', teams_df)
    
    # ==================== PLAYERS OPERATIONS ====================
    
    def create_player(self, player_data: Dict) -> int:
        """Create a new player"""
        players_df = self._read_table('players')
        player_id = len(players_df) + 1
        
        player_data['player_id'] = player_id
        player_data['auction_status'] = 'unsold'
        
        new_player = pd.DataFrame([player_data])
        players_df = pd.concat([players_df, new_player], ignore_index=True)
        self._write_table('players', players_df)
        return player_id
    
    def get_player(self, player_id: int) -> Optional[Dict]:
        """Get player by ID"""
        players_df = self._read_table('players')
        player = players_df[players_df['player_id'] == player_id]
        return player.to_dict('records')[0] if not player.empty else None
    
    def get_player_by_name(self, player_name: str) -> Optional[Dict]:
        """Get player by name"""
        players_df = self._read_table('players')
        player = players_df[players_df['player_name'] == player_name]
        return player.to_dict('records')[0] if not player.empty else None
    
    def get_all_players(self) -> pd.DataFrame:
        """Get all players"""
        return self._read_table('players')
    
    def get_players_by_category(self, category: str) -> pd.DataFrame:
        """Get players by category"""
        players_df = self._read_table('players')
        return players_df[players_df['category'] == category]
    
    def get_players_by_set(self, set_number: int) -> pd.DataFrame:
        """Get players by auction set"""
        players_df = self._read_table('players')
        return players_df[players_df['set_number'] == set_number]
    
    def update_player(self, player_id: int, updates: Dict):
        """Update player information"""
        players_df = self._read_table('players')
        for key, value in updates.items():
            players_df.loc[players_df['player_id'] == player_id, key] = value
        self._write_table('players', players_df)
    
    # ==================== AUCTION BIDS OPERATIONS ====================
    
    def create_bid(self, player_id: int, team_id: int, bid_amount: float, 
                   is_final: bool = False) -> int:
        """Create a new bid"""
        bids_df = self._read_table('auction_bids')
        bid_id = len(bids_df) + 1
        
        new_bid = pd.DataFrame([{
            'bid_id': bid_id,
            'player_id': player_id,
            'team_id': team_id,
            'bid_amount': bid_amount,
            'timestamp': pd.Timestamp.now(),
            'is_final': is_final
        }])
        
        bids_df = pd.concat([bids_df, new_bid], ignore_index=True)
        self._write_table('auction_bids', bids_df)
        return bid_id
    
    def get_bids_for_player(self, player_id: int) -> pd.DataFrame:
        """Get all bids for a player"""
        bids_df = self._read_table('auction_bids')
        return bids_df[bids_df['player_id'] == player_id]
    
    def get_final_bid(self, player_id: int) -> Optional[Dict]:
        """Get final bid for a player"""
        bids_df = self._read_table('auction_bids')
        final_bid = bids_df[(bids_df['player_id'] == player_id) & 
                           (bids_df['is_final'] == True)]
        return final_bid.to_dict('records')[0] if not final_bid.empty else None
    
    # ==================== TEAM SQUADS OPERATIONS ====================
    
    def add_player_to_squad(self, team_id: int, player_id: int, purchase_price: float):
        """Add player to team squad"""
        squads_df = self._read_table('team_squads')
        squad_id = len(squads_df) + 1
        
        new_entry = pd.DataFrame([{
            'squad_id': squad_id,
            'team_id': team_id,
            'player_id': player_id,
            'purchase_price': purchase_price
        }])
        
        squads_df = pd.concat([squads_df, new_entry], ignore_index=True)
        self._write_table('team_squads', squads_df)
    
    def get_team_squad(self, team_id: int) -> pd.DataFrame:
        """Get all players in a team's squad"""
        squads_df = self._read_table('team_squads')
        return squads_df[squads_df['team_id'] == team_id]
    
    # ==================== PLAYER STATS OPERATIONS ====================
    
    def save_player_stats(self, stats_df: pd.DataFrame):
        """Save player statistics"""
        existing_stats = self._read_table('player_stats')
        
        # Add stat_id if not present
        if 'stat_id' not in stats_df.columns:
            start_id = len(existing_stats) + 1
            stats_df['stat_id'] = range(start_id, start_id + len(stats_df))
        
        combined = pd.concat([existing_stats, stats_df], ignore_index=True)
        self._write_table('player_stats', combined)
    
    def get_player_stats(self, player_name: str) -> pd.DataFrame:
        """Get statistics for a player"""
        stats_df = self._read_table('player_stats')
        return stats_df[stats_df['player_name'] == player_name]
    
    # ==================== FANTASY POINTS OPERATIONS ====================
    
    def save_fantasy_points(self, points_df: pd.DataFrame):
        """Save fantasy points"""
        existing_points = self._read_table('fantasy_points')
        
        # Add point_id if not present
        if 'point_id' not in points_df.columns:
            start_id = len(existing_points) + 1
            points_df['point_id'] = range(start_id, start_id + len(points_df))
        
        combined = pd.concat([existing_points, points_df], ignore_index=True)
        self._write_table('fantasy_points', combined)
    
    def get_fantasy_points(self, player_name: str) -> pd.DataFrame:
        """Get fantasy points for a player"""
        points_df = self._read_table('fantasy_points')
        return points_df[points_df['player_name'] == player_name]
    
    def get_all_fantasy_points(self) -> pd.DataFrame:
        """Get all fantasy points"""
        return self._read_table('fantasy_points')
    
    # ==================== PREDICTIONS OPERATIONS ====================
    
    def save_predictions(self, predictions_df: pd.DataFrame):
        """Save predictions"""
        existing_predictions = self._read_table('predictions')
        
        # Add prediction_id if not present
        if 'prediction_id' not in predictions_df.columns:
            start_id = len(existing_predictions) + 1
            predictions_df['prediction_id'] = range(start_id, start_id + len(predictions_df))
        
        # Add prediction date
        if 'prediction_date' not in predictions_df.columns:
            predictions_df['prediction_date'] = pd.Timestamp.now()
        
        combined = pd.concat([existing_predictions, predictions_df], ignore_index=True)
        self._write_table('predictions', combined)
    
    def get_predictions(self, player_name: str) -> pd.DataFrame:
        """Get predictions for a player"""
        predictions_df = self._read_table('predictions')
        return predictions_df[predictions_df['player_name'] == player_name]
    
    def get_all_predictions(self) -> pd.DataFrame:
        """Get all predictions"""
        return self._read_table('predictions')
    
    # ==================== UTILITY METHODS ====================
    
    def _read_table(self, table_name: str) -> pd.DataFrame:
        """Read a CSV table"""
        file_path = self.db_path / TABLES[table_name]
        return pd.read_csv(file_path)
    
    def _write_table(self, table_name: str, df: pd.DataFrame):
        """Write a CSV table"""
        file_path = self.db_path / TABLES[table_name]
        df.to_csv(file_path, index=False)
    
    def clear_all_tables(self):
        """Clear all tables (use with caution)"""
        self._initialize_tables()
    
    def export_database(self, export_path: str):
        """Export entire database to a directory"""
        export_path = Path(export_path)
        export_path.mkdir(parents=True, exist_ok=True)
        
        for table_name in TABLES.keys():
            df = self._read_table(table_name)
            df.to_csv(export_path / TABLES[table_name], index=False)
