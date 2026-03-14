"""
Data Processing Pipeline
Processes raw JSON data and generates player statistics
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict
from src.config.constants import RAW_DATA_PATH, PROCESSED_DATA_PATH
from src.scoring.fantasy_points_engine import FantasyPointsEngine


class DataProcessor:
    """
    Processes raw match data and generates aggregated player statistics
    """
    
    def __init__(self):
        self.scoring_engine = FantasyPointsEngine()
        self.raw_path = Path(RAW_DATA_PATH)
        self.processed_path = Path(PROCESSED_DATA_PATH)
        self.processed_path.mkdir(parents=True, exist_ok=True)
    
    def process_all_matches(self) -> pd.DataFrame:
        """
        Process all match JSON files and generate fantasy points
        
        Returns:
            DataFrame with all player fantasy points across all matches
        """
        all_points = []
        
        json_files = list(self.raw_path.glob('*.json'))
        print(f"Processing {len(json_files)} match files...")
        
        for idx, json_file in enumerate(json_files, 1):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    match_data = json.load(f)
                
                # Process match and calculate fantasy points
                match_points = self.scoring_engine.process_match_data(match_data)
                
                # Add match metadata
                match_points['season'] = match_data.get('info', {}).get('season', 'unknown')
                match_points['venue'] = match_data.get('info', {}).get('venue', 'unknown')
                match_points['date'] = match_data.get('info', {}).get('dates', ['unknown'])[0]
                
                all_points.append(match_points)
                
                if idx % 50 == 0:
                    print(f"Processed {idx}/{len(json_files)} matches...")
                    
            except Exception as e:
                print(f"Error processing {json_file.name}: {str(e)}")
                continue
        
        # Combine all match data
        if all_points:
            combined_df = pd.concat(all_points, ignore_index=True)
            
            # Save processed data
            output_file = self.processed_path / 'all_fantasy_points.csv'
            combined_df.to_csv(output_file, index=False)
            print(f"\nSaved processed data to {output_file}")
            
            return combined_df
        else:
            return pd.DataFrame()
    
    def generate_player_aggregates(self, fantasy_points_df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate aggregated player statistics
        
        Args:
            fantasy_points_df: DataFrame with fantasy points per match
        
        Returns:
            DataFrame with aggregated player statistics
        """
        aggregates = fantasy_points_df.groupby('player_name').agg({
            'total_points': ['sum', 'mean', 'std', 'max', 'min'],
            'batting_points': ['sum', 'mean'],
            'bowling_points': ['sum', 'mean'],
            'fielding_points': ['sum', 'mean'],
            'runs': ['sum', 'mean', 'max'],
            'wickets': ['sum', 'mean', 'max'],
            'catches': ['sum', 'mean'],
            'match_id': 'count'  # Total matches
        }).reset_index()
        
        # Flatten column names
        aggregates.columns = ['_'.join(col).strip('_') for col in aggregates.columns.values]
        aggregates.rename(columns={'match_id_count': 'total_matches'}, inplace=True)
        
        # Calculate points per match
        aggregates['points_per_match'] = aggregates['total_points_sum'] / aggregates['total_matches']
        
        # Save aggregates
        output_file = self.processed_path / 'player_aggregates.csv'
        aggregates.to_csv(output_file, index=False)
        print(f"Saved player aggregates to {output_file}")
        
        return aggregates
    
    def load_players_from_excel(self, excel_path: str) -> pd.DataFrame:
        """
        Load player list from PLAYERS_RULES.xlsx
        
        Args:
            excel_path: Path to Excel file
        
        Returns:
            DataFrame with player information
        """
        # Read Players sheet
        players_df = pd.read_excel(excel_path, sheet_name='Players', header=None)

        players_list = []
        
        # Process each set
        set_mapping = {
            'SET 1 - BOWLERS': ('BOWL', 1),
            'SET 2 - BATSMAN': ('BAT', 2),
            'SET 3 - ALL ROUNDERS': ('AR', 3),
            'SET 4 - WICKET KEEPERS': ('WK', 4),
            'SET 5 - BOWLERS': ('BOWL', 5),
            'SET 6 - BATSMAN': ('BAT', 6),
            'SET 7 - ALL ROUNDERS': ('AR', 7),
            'SET 8 - WICKET KEEPERS': ('WK', 8),
        }
        
        # Parse the Excel structure
        for col_idx in range(0, players_df.shape[1], 3):
            if col_idx + 2 < players_df.shape[1]:
                set_header = players_df.iloc[0, col_idx + 1]
                
                if set_header in set_mapping:
                    category, set_num = set_mapping[set_header]
                    
                    # Extract players from this set
                    for row_idx in range(2, players_df.shape[0]):
                        player_num = players_df.iloc[row_idx, col_idx]
                        player_name = players_df.iloc[row_idx, col_idx + 1]
                        base_price = players_df.iloc[row_idx, col_idx + 2]
                        
                        if pd.notna(player_name) and player_name not in ['ACCELERATED AUCTION', 'BOWLERS', 'BATSMAN', 'ALL ROUNDERS', 'WICKET KEEPERS']:
                            # Parse base price
                            if pd.notna(base_price):
                                price_str = str(base_price)
                                if 'Cr' in price_str:
                                    price = float(price_str.replace('Cr', '').strip())
                                elif 'L' in price_str:
                                    price = float(price_str.replace('L', '').strip()) / 100
                                else:
                                    price = 1.0
                            else:
                                price = 0.25  # Default for accelerated auction
                            
                            players_list.append({
                                'player_name': player_name,
                                'category': category,
                                'base_price': price,
                                'set_number': set_num,
                                'is_overseas': self._is_overseas_player(player_name)
                            })
        
        players_df = pd.DataFrame(players_list)
        
        # Save to processed data
        output_file = self.processed_path / 'auction_players.csv'
        players_df.to_csv(output_file, index=False)
        print(f"Loaded {len(players_df)} players from Excel")
        
        return players_df

    def load_players_from_excel_v1(self, excel_path: str) -> pd.DataFrame:
        """
        Load player list from PLAYERS_RULES.xlsx

        Args:
            excel_path: Path to Excel file

        Returns:
            DataFrame with player information
        """
        # Read Players sheet
        players_df = pd.read_excel(excel_path, sheet_name='Players_structured', header=0)


        # players_df = pd.DataFrame()
        players_df['is_overseas'] = players_df['player_name'].apply(lambda x: self._is_overseas_player(x))

        # Save to processed data
        output_file = self.processed_path / 'auction_players.csv'
        players_df.to_csv(output_file, index=False)
        print(f"Loaded {len(players_df)} players from Excel")

        return players_df

    def _is_overseas_player(self, player_name: str) -> bool:
        """
        Determine if a player is overseas (simplified logic)
        """
        # Common overseas first names/patterns
        overseas_indicators = [
            'Josh', 'Trent', 'Mitchell', 'Kagiso', 'Jos', 'Heinrich', 'Nicholas',
            'Travis', 'Cameron', 'Sam', 'Pat', 'Rashid', 'Sunil', 'Glenn', 'Tim',
            'Marco', 'Jofra', 'Nathan', 'Shimron', 'Finn', 'Tristan', 'David',
            'Pathum', 'Dewald', 'Marcus', 'Azmatullah', 'Nitish Kumar', 'Matthew',
            'Jacob', 'Liam', 'Jason', 'Donovan', 'Brydon', 'Corbin', 'Wanindu',
            'Cooper', 'Jordan', 'Lhuan', 'Kamindu', 'Jamie', 'Zak', 'Jack',
            'Kyle', 'Matt', 'Adam', 'Nuwan', 'Dushmantha', 'Kwena', 'Anrich',
            'Ben', 'Luke', 'Lockie', 'Xavier', 'Nandre', 'Lungi', 'Akeal',
            'Matheesha'
        ]
        
        for indicator in overseas_indicators:
            if indicator in player_name:
                return True
        return False
    
    def merge_player_data(self, players_df: pd.DataFrame, 
                         aggregates_df: pd.DataFrame) -> pd.DataFrame:
        """
        Merge player auction data with historical statistics
        
        Args:
            players_df: Player auction information
            aggregates_df: Historical player statistics
        
        Returns:
            Merged DataFrame
        """
        merged = players_df.merge(
            aggregates_df,
            on='player_name',
            how='left'
        )
        
        # Fill NaN values for players without historical data
        numeric_cols = merged.select_dtypes(include=[np.number]).columns
        merged[numeric_cols] = merged[numeric_cols].fillna(0)
        
        # Save merged data
        output_file = self.processed_path / 'players_with_stats.csv'
        merged.to_csv(output_file, index=False)
        print(f"Saved merged player data to {output_file}")
        
        return merged
    
    def generate_feature_matrix(self, merged_df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate feature matrix for ML models
        
        Args:
            merged_df: Merged player data
        
        Returns:
            Feature matrix DataFrame
        """
        features = merged_df.copy()
        
        # Create derived features
        features['value_score'] = features['points_per_match'] / (features['base_price'] + 0.1)
        features['consistency_score'] = features['total_points_mean'] / (features['total_points_std'] + 1)
        features['batting_specialist'] = (features['batting_points_mean'] > features['bowling_points_mean']).astype(int)
        features['bowling_specialist'] = (features['bowling_points_mean'] > features['batting_points_mean']).astype(int)
        features['all_rounder'] = ((features['batting_points_mean'] > 10) & 
                                   (features['bowling_points_mean'] > 10)).astype(int)
        
        # Category encoding
        features = pd.get_dummies(features, columns=['category'], prefix='cat')
        
        # Save feature matrix
        output_file = self.processed_path / 'feature_matrix.csv'
        features.to_csv(output_file, index=False)
        print(f"Saved feature matrix to {output_file}")
        
        return features
