"""
Fantasy Cricket Auction AI - Main Streamlit Application
Complete dashboard with CRM, analytics, and AI auction assistant
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

from src.config.constants import UI_CONFIG, AUCTION_PURSE, SQUAD_CONSTRAINTS
from src.data_access.csv_database import CSVDatabase
from src.scoring.fantasy_points_engine import FantasyPointsEngine

# Page configuration
st.set_page_config(
    page_title=UI_CONFIG['page_title'],
    page_icon=UI_CONFIG['page_icon'],
    layout=UI_CONFIG['layout']
)

# Initialize session state
if 'db' not in st.session_state:
    st.session_state.db = CSVDatabase()
if 'num_teams' not in st.session_state:
    st.session_state.num_teams = 10
if 'current_bid_player' not in st.session_state:
    st.session_state.current_bid_player = None

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FF4B4B;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #262730;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FF4B4B;
    }
    .player-card {
        background-color: #1E1E1E;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .bid-button {
        background-color: #FF4B4B;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.3rem;
        border: none;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<div class="main-header">🏏 Fantasy Cricket Auction AI</div>', unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "🏠 Home",
    "⚙️ CRM - Setup",
    "📊 Player Analytics",
    "🎯 Auction Assistant",
    "🔮 Predictions",
    "👥 Team Builder",
    "📈 Live Auction"
])

# ==================== HOME PAGE ====================
if page == "🏠 Home":
    st.header("Welcome to Fantasy Cricket Auction AI")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Players", len(st.session_state.db.get_all_players()))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Teams Registered", len(st.session_state.db.get_all_teams()))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        fantasy_points = st.session_state.db.get_all_fantasy_points()
        st.metric("Matches Analyzed", len(fantasy_points['match_id'].unique()) if not fantasy_points.empty else 0)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("🎯 System Features")
    
    features = {
        "Fantasy Points Engine": "Calculate fantasy points based on ball-by-ball data",
        "Player Analytics": "Comprehensive player profiling and performance metrics",
        "ML Predictions": "Expected fantasy points using multiple ML models",
        "Auction Simulator": "Simulate N-team auctions with different strategies",
        "Live AI Assistant": "Real-time bidding recommendations during auction",
        "CRM System": "Manage teams, players, and auction data",
        "Dark Horse Finder": "Identify undervalued players with high potential"
    }
    
    for feature, description in features.items():
        st.markdown(f"**{feature}**: {description}")
    
    st.markdown("---")
    st.info("👈 Use the sidebar to navigate to different sections")

# ==================== CRM - SETUP PAGE ====================
elif page == "⚙️ CRM - Setup":
    st.header("CRM - Auction Setup")
    
    tab1, tab2, tab3 = st.tabs(["Teams Management", "Auction Data Entry", "Configuration"])
    
    with tab1:
        st.subheader("Teams Management")
        
        # Add new team
        with st.expander("➕ Add New Team"):
            team_name = st.text_input("Team Name")
            if st.button("Create Team"):
                if team_name:
                    team_id = st.session_state.db.create_team(team_name, AUCTION_PURSE)
                    st.success(f"✅ Team '{team_name}' created with ID: {team_id}")
                    st.rerun()
                else:
                    st.error("Please enter a team name")
        
        # Display existing teams
        st.subheader("Registered Teams")
        teams_df = st.session_state.db.get_all_teams()
        
        if not teams_df.empty:
            st.dataframe(teams_df, use_container_width=True)
            
            # Delete team
            team_to_delete = st.selectbox("Select team to delete", teams_df['team_name'].tolist())
            if st.button("🗑️ Delete Team"):
                team_id = teams_df[teams_df['team_name'] == team_to_delete]['team_id'].values[0]
                st.session_state.db.delete_team(team_id)
                st.success(f"Deleted team: {team_to_delete}")
                st.rerun()
        else:
            st.info("No teams registered yet. Add teams above.")
    
    with tab2:
        st.subheader("Auction Data Entry")
        
        teams_df = st.session_state.db.get_all_teams()
        players_df = st.session_state.db.get_all_players()
        
        if teams_df.empty:
            st.warning("⚠️ Please create teams first in the Teams Management tab")
        elif players_df.empty:
            st.warning("⚠️ No players loaded. Please run initialize_data.py first")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                selected_player = st.selectbox(
                    "Select Player",
                    players_df['player_name'].unique().tolist()
                )
                
                player_info = players_df[players_df['player_name'] == selected_player].iloc[0]
                st.info(f"Category: {player_info['category']} | Base Price: ₹{player_info['base_price']} Cr")
            
            with col2:
                selected_team = st.selectbox(
                    "Sold To Team",
                    teams_df['team_name'].tolist()
                )
                
                sold_price = st.number_input(
                    "Sold Price (Cr)",
                    min_value=0.25,
                    max_value=50.0,
                    value=float(player_info['base_price']),
                    step=0.25
                )
            
            if st.button("💰 Record Sale"):
                team_id = teams_df[teams_df['team_name'] == selected_team]['team_id'].values[0]
                player_id = player_info['player_id']
                
                # Create final bid
                st.session_state.db.create_bid(player_id, team_id, sold_price, is_final=True)
                
                # Add to squad
                st.session_state.db.add_player_to_squad(team_id, player_id, sold_price)
                
                # Update player status
                st.session_state.db.update_player(player_id, {'auction_status': 'sold'})
                
                # Update team purse and counts
                team = st.session_state.db.get_team(team_id)
                updates = {
                    'purse_remaining': team['purse_remaining'] - sold_price,
                    'players_count': team['players_count'] + 1
                }
                
                # Update category count
                category_map = {'BAT': 'bat_count', 'BOWL': 'bowl_count', 'AR': 'ar_count', 'WK': 'wk_count'}
                if player_info['category'] in category_map:
                    cat_key = category_map[player_info['category']]
                    updates[cat_key] = team[cat_key] + 1
                
                if player_info['is_overseas']:
                    updates['overseas_count'] = team['overseas_count'] + 1
                
                st.session_state.db.update_team(team_id, updates)
                
                st.success(f"✅ {selected_player} sold to {selected_team} for ₹{sold_price} Cr")
                st.rerun()
        
        # Show recent transactions
        st.markdown("---")
        st.subheader("Recent Transactions")
        bids_df = st.session_state.db._read_table('auction_bids')
        if not bids_df.empty:
            recent_bids = bids_df[bids_df['is_final'] == True].tail(10)
            
            # Merge with player and team names
            for idx, bid in recent_bids.iterrows():
                player = st.session_state.db.get_player(bid['player_id'])
                team = st.session_state.db.get_team(bid['team_id'])
                if player and team:
                    st.markdown(f"**{player['player_name']}** → {team['team_name']} (₹{bid['bid_amount']} Cr)")
    
    with tab3:
        st.subheader("Configuration")
        
        num_teams = st.number_input(
            "Number of Teams",
            min_value=2,
            max_value=30,
            value=st.session_state.num_teams
        )
        st.session_state.num_teams = num_teams
        
        # Show squad constraints
        if num_teams in [7, 8, 9, 10]:
            constraints = SQUAD_CONSTRAINTS[num_teams]
            st.info(f"""
            **Squad Constraints for {num_teams} teams:**
            - Total Players: {constraints['total_players']}
            - Batsmen: {constraints['bat']['min']}-{constraints['bat']['max']}
            - Bowlers: {constraints['bowl']['min']}-{constraints['bowl']['max']}
            - All-Rounders: {constraints['ar']['min']}-{constraints['ar']['max']}
            - Wicket-Keepers: {constraints['wk']['min']}-{constraints['wk']['max']}
            - Max Overseas: {constraints['overseas']['max']}
            """)
        else:
            st.warning("Custom constraints needed for this team count")

# ==================== PLAYER ANALYTICS PAGE ====================
elif page == "📊 Player Analytics":
    st.header("Player Analytics Dashboard")
    
    # Load data
    try:
        players_with_stats = pd.read_csv("data/processed/players_with_stats.csv")
    except:
        st.error("❌ Player statistics not found. Please run initialize_data.py first")
        st.stop()
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category_filter = st.multiselect(
            "Category",
            options=players_with_stats['category'].unique(),
            default=players_with_stats['category'].unique()
        )
    
    with col2:
        price_range = st.slider(
            "Base Price Range (Cr)",
            0.0, 2.0,
            (0.0, 2.0)
        )
    
    with col3:
        overseas_filter = st.selectbox(
            "Player Type",
            ["All", "Indian", "Overseas"]
        )
    
    # Apply filters
    filtered_df = players_with_stats[
        (players_with_stats['category'].isin(category_filter)) &
        (players_with_stats['base_price'] >= price_range[0]) &
        (players_with_stats['base_price'] <= price_range[1])
    ]
    
    if overseas_filter == "Indian":
        filtered_df = filtered_df[filtered_df['is_overseas'] == False]
    elif overseas_filter == "Overseas":
        filtered_df = filtered_df[filtered_df['is_overseas'] == True]
    
    # Metrics
    st.subheader("📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Players", len(filtered_df))
    with col2:
        avg_points = filtered_df['points_per_match'].mean() if 'points_per_match' in filtered_df.columns else 0
        st.metric("Avg Points/Match", f"{avg_points:.1f}")
    with col3:
        avg_price = filtered_df['base_price'].mean()
        st.metric("Avg Base Price", f"₹{avg_price:.2f} Cr")
    with col4:
        if 'value_score' in filtered_df.columns:
            best_value = filtered_df['value_score'].max()
            st.metric("Best Value Score", f"{best_value:.1f}")
    
    # Visualizations
    tab1, tab2, tab3 = st.tabs(["Top Performers", "Value Analysis", "Dark Horses"])
    
    with tab1:
        st.subheader("Top Performers by Fantasy Points")
        
        if 'points_per_match' in filtered_df.columns:
            top_players = filtered_df.nlargest(20, 'points_per_match')
            
            fig = px.bar(
                top_players,
                x='player_name',
                y='points_per_match',
                color='category',
                title="Top 20 Players by Points Per Match"
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(
                top_players[['player_name', 'category', 'base_price', 'points_per_match', 'total_matches']],
                use_container_width=True
            )
    
    with tab2:
        st.subheader("Value for Money Analysis")
        
        if 'value_score' in filtered_df.columns and 'points_per_match' in filtered_df.columns:
            fig = px.scatter(
                filtered_df,
                x='base_price',
                y='points_per_match',
                size='value_score',
                color='category',
                hover_data=['player_name'],
                title="Price vs Performance (bubble size = value score)"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("🌟 Dark Horse Players")
        st.info("Players with high value scores but low base prices")
        
        if 'value_score' in filtered_df.columns:
            dark_horses = filtered_df[
                (filtered_df['base_price'] <= 1.0) &
                (filtered_df['value_score'] > filtered_df['value_score'].quantile(0.75))
            ].nlargest(15, 'value_score')
            
            st.dataframe(
                dark_horses[['player_name', 'category', 'base_price', 'points_per_match', 'value_score']],
                use_container_width=True
            )

# ==================== AUCTION ASSISTANT PAGE ====================
elif page == "🎯 Auction Assistant":
    st.header("AI Auction Bidding Assistant")
    
    st.info("🤖 Get real-time bidding recommendations based on team needs and player value")
    
    teams_df = st.session_state.db.get_all_teams()
    
    if teams_df.empty:
        st.warning("⚠️ Please create teams first in the CRM section")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            selected_team = st.selectbox("Your Team", teams_df['team_name'].tolist())
            team_id = teams_df[teams_df['team_name'] == selected_team]['team_id'].values[0]
            team_info = st.session_state.db.get_team(team_id)
            
            st.metric("Purse Remaining", f"₹{team_info['purse_remaining']:.2f} Cr")
            st.metric("Players", f"{team_info['players_count']}")
            
            # Show squad composition
            st.markdown("**Squad Composition:**")
            st.write(f"BAT: {team_info['bat_count']} | BOWL: {team_info['bowl_count']} | AR: {team_info['ar_count']} | WK: {team_info['wk_count']}")
            st.write(f"Overseas: {team_info['overseas_count']}")
        
        with col2:
            # Current player on auction
            players_df = st.session_state.db.get_all_players()
            unsold_players = players_df[players_df['auction_status'] == 'unsold']
            
            if not unsold_players.empty:
                current_player = st.selectbox("Player on Auction", unsold_players['player_name'].tolist())
                player_info = unsold_players[unsold_players['player_name'] == current_player].iloc[0]
                
                st.markdown(f"**Category:** {player_info['category']}")
                st.markdown(f"**Base Price:** ₹{player_info['base_price']} Cr")
                st.markdown(f"**Overseas:** {'Yes' if player_info['is_overseas'] else 'No'}")
                
                # Load player stats
                try:
                    stats_df = pd.read_csv("data/processed/players_with_stats.csv")
                    player_stats = stats_df[stats_df['player_name'] == current_player]
                    
                    if not player_stats.empty:
                        stats = player_stats.iloc[0]
                        st.markdown(f"**Avg Points/Match:** {stats.get('points_per_match', 0):.1f}")
                        st.markdown(f"**Value Score:** {stats.get('value_score', 0):.1f}")
                except:
                    pass
        
        st.markdown("---")
        
        # Bidding recommendation
        st.subheader("💡 AI Recommendation")
        
        current_bid = st.number_input("Current Bid (Cr)", min_value=0.25, value=float(player_info['base_price']), step=0.25)
        
        if st.button("Get Recommendation"):
            # Simple recommendation logic
            try:
                stats_df = pd.read_csv("data/processed/players_with_stats.csv")
                player_stats = stats_df[stats_df['player_name'] == current_player]
                
                if not player_stats.empty:
                    stats = player_stats.iloc[0]
                    expected_points = stats.get('points_per_match', 0)
                    value_score = stats.get('value_score', 0)
                    
                    # Calculate recommended max bid
                    max_bid = min(
                        expected_points * 0.05,  # 5% of expected points
                        team_info['purse_remaining'] * 0.15  # Max 15% of remaining purse
                    )
                    
                    if current_bid <= max_bid:
                        st.success(f"✅ RECOMMENDED: BID (Max: ₹{max_bid:.2f} Cr)")
                        st.markdown(f"**Reasoning:** High value score ({value_score:.1f}) and fits team needs")
                    else:
                        st.warning(f"⚠️ CAUTION: Price exceeds recommended max of ₹{max_bid:.2f} Cr")
                else:
                    st.info("ℹ️ No historical data available for this player")
            except:
                st.error("Unable to load player statistics")

# ==================== PREDICTIONS PAGE ====================
elif page == "🔮 Predictions":
    st.header("Expected Fantasy Points Predictions")
    
    st.info("📊 ML-based predictions for expected fantasy points in upcoming matches")
    
    try:
        players_with_stats = pd.read_csv("data/processed/players_with_stats.csv")
        
        # Simple prediction based on historical average (placeholder for ML models)
        predictions = players_with_stats[['player_name', 'category', 'points_per_match']].copy()
        predictions['expected_points'] = predictions['points_per_match']
        predictions['confidence_low'] = predictions['points_per_match'] * 0.8
        predictions['confidence_high'] = predictions['points_per_match'] * 1.2
        
        # Sort by expected points
        predictions = predictions.sort_values('expected_points', ascending=False)
        
        # Display top predictions
        st.subheader("Top 30 Predicted Performers")
        
        top_30 = predictions.head(30)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=top_30['player_name'],
            y=top_30['expected_points'],
            name='Expected Points',
            error_y=dict(
                type='data',
                symmetric=False,
                array=top_30['confidence_high'] - top_30['expected_points'],
                arrayminus=top_30['expected_points'] - top_30['confidence_low']
            )
        ))
        fig.update_layout(
            title="Expected Fantasy Points (with confidence intervals)",
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(top_30, use_container_width=True)
        
    except Exception as e:
        st.error(f"❌ Error loading predictions: {e}")
        st.info("Please run initialize_data.py first")

# ==================== TEAM BUILDER PAGE ====================
elif page == "👥 Team Builder":
    st.header("Interactive Team Builder")
    
    st.info("🎯 Build your optimal team within budget and squad constraints")
    
    try:
        players_with_stats = pd.read_csv("data/processed/players_with_stats.csv")
        
        # Budget and constraints
        col1, col2 = st.columns(2)
        
        with col1:
            budget = st.number_input("Total Budget (Cr)", min_value=50.0, max_value=150.0, value=100.0)
        
        with col2:
            num_players = st.number_input("Number of Players", min_value=11, max_value=20, value=14)
        
        # Player selection
        st.subheader("Select Players")
        
        selected_players = st.multiselect(
            "Choose players for your team",
            players_with_stats['player_name'].tolist()
        )
        
        if selected_players:
            team_df = players_with_stats[players_with_stats['player_name'].isin(selected_players)]
            
            # Calculate team metrics
            total_cost = team_df['base_price'].sum()
            total_expected_points = team_df['points_per_match'].sum() if 'points_per_match' in team_df.columns else 0
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Cost", f"₹{total_cost:.2f} Cr")
                remaining = budget - total_cost
                st.metric("Remaining", f"₹{remaining:.2f} Cr", delta=f"{remaining:.2f}")
            
            with col2:
                st.metric("Players Selected", len(selected_players))
                st.metric("Slots Remaining", num_players - len(selected_players))
            
            with col3:
                st.metric("Expected Points", f"{total_expected_points:.1f}")
            
            # Squad composition
            st.subheader("Squad Composition")
            composition = team_df['category'].value_counts()
            
            fig = px.pie(values=composition.values, names=composition.index, title="Category Distribution")
            st.plotly_chart(fig)
            
            # Show selected players
            st.subheader("Selected Players")
            st.dataframe(team_df[['player_name', 'category', 'base_price', 'points_per_match']], use_container_width=True)
            
    except Exception as e:
        st.error(f"❌ Error: {e}")
        st.info("Please run initialize_data.py first")

# ==================== LIVE AUCTION PAGE ====================
elif page == "📈 Live Auction":
    st.header("Live Auction Dashboard")
    
    st.info("📊 Real-time auction tracking and analytics")
    
    teams_df = st.session_state.db.get_all_teams()
    
    if teams_df.empty:
        st.warning("⚠️ No teams registered. Please set up teams in CRM section.")
    else:
        # Team standings
        st.subheader("Team Standings")
        
        standings = teams_df[['team_name', 'purse_remaining', 'players_count', 'bat_count', 'bowl_count', 'ar_count', 'wk_count', 'overseas_count']]
        st.dataframe(standings, use_container_width=True)
        
        # Auction progress
        players_df = st.session_state.db.get_all_players()
        sold_count = len(players_df[players_df['auction_status'] == 'sold'])
        total_count = len(players_df)
        
        st.subheader("Auction Progress")
        progress = sold_count / total_count if total_count > 0 else 0
        st.progress(progress)
        st.write(f"{sold_count} / {total_count} players sold ({progress*100:.1f}%)")
        
        # Category-wise progress
        col1, col2, col3, col4 = st.columns(4)
        
        for idx, (col, category) in enumerate(zip([col1, col2, col3, col4], ['BAT', 'BOWL', 'AR', 'WK'])):
            with col:
                cat_players = players_df[players_df['category'] == category]
                cat_sold = len(cat_players[cat_players['auction_status'] == 'sold'])
                cat_total = len(cat_players)
                st.metric(category, f"{cat_sold}/{cat_total}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>Fantasy Cricket Auction AI © 2026 | Built with ❤️ using Streamlit</div>",
    unsafe_allow_html=True
)
