"""
Data Initialization Script
Run this script to process all raw data and prepare the system
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.utils.data_processor import DataProcessor
from src.data_access.csv_database import CSVDatabase
import pandas as pd


def main():
    """Main initialization function"""
    print("=" * 60)
    print("FANTASY CRICKET AUCTION AI - DATA INITIALIZATION")
    print("=" * 60)
    
    # Initialize components
    processor = DataProcessor()
    db = CSVDatabase()
    
    print("\n[1/5] Processing match data and calculating fantasy points...")
    try:
        fantasy_points_df = processor.process_all_matches()
        print(f"✓ Processed {len(fantasy_points_df)} player-match records")
    except Exception as e:
        print(f"✗ Error processing matches: {e}")
        fantasy_points_df = pd.DataFrame()
    
    print("\n[2/5] Generating player aggregates...")
    try:
        if not fantasy_points_df.empty:
            aggregates_df = processor.generate_player_aggregates(fantasy_points_df)
            print(f"✓ Generated aggregates for {len(aggregates_df)} players")
        else:
            print("⚠ Skipping aggregates (no fantasy points data)")
            aggregates_df = pd.DataFrame()
    except Exception as e:
        print(f"✗ Error generating aggregates: {e}")
        aggregates_df = pd.DataFrame()
    
    print("\n[3/5] Loading auction players from Excel...")
    try:
        excel_path = "PLAYERS_RULES.xlsx"
        players_df = processor.load_players_from_excel_v1(excel_path)
        print(f"✓ Loaded {len(players_df)} auction players")
    except Exception as e:
        print(f"✗ Error loading players: {e}")
        players_df = pd.DataFrame()
    
    print("\n[4/5] Merging player data with statistics...")
    try:
        if not players_df.empty and not aggregates_df.empty:
            merged_df = processor.merge_player_data(players_df, aggregates_df)
            print(f"✓ Merged data for {len(merged_df)} players")
            
            # Generate feature matrix
            features_df = processor.generate_feature_matrix(merged_df)
            print(f"✓ Generated feature matrix with {features_df.shape[1]} features")
        else:
            print("⚠ Skipping merge (missing data)")
            merged_df = players_df if not players_df.empty else pd.DataFrame()
    except Exception as e:
        print(f"✗ Error merging data: {e}")
        merged_df = players_df if not players_df.empty else pd.DataFrame()
    
    print("\n[5/5] Initializing database...")
    try:
        # Save fantasy points to database
        if not fantasy_points_df.empty:
            db.save_fantasy_points(fantasy_points_df)
            print(f"✓ Saved fantasy points to database")
        
        # Load players into database
        if not merged_df.empty:
            for _, player in merged_df.iterrows():
                player_data = {
                    'player_name': player['player_name'],
                    'category': player['category'],
                    'base_price': player['base_price'],
                    'is_overseas': player['is_overseas'],
                    'set_number': player['set_number']
                }
                db.create_player(player_data)
            print(f"✓ Loaded {len(merged_df)} players into database")
        
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
    
    print("\n" + "=" * 60)
    print("DATA INITIALIZATION COMPLETE!")
    print("=" * 60)
    print("\nYou can now run the application:")
    print("  streamlit run frontend/app.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
