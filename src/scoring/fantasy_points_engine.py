"""
Fantasy Points Scoring Engine
Calculates fantasy points based on ball-by-ball data and scoring rules
"""

from typing import Dict, List, Tuple
import pandas as pd
import numpy as np
from ..config.constants import SCORING_RULES


class FantasyPointsEngine:
    """
    Core engine for calculating fantasy points from match data
    Implements SOLID principles with single responsibility
    """
    
    def __init__(self):
        self.rules = SCORING_RULES
    
    def calculate_batting_points(self, player_stats: Dict) -> float:
        """
        Calculate batting fantasy points for a player
        
        Args:
            player_stats: Dictionary containing batting statistics
                - runs: Total runs scored
                - balls_faced: Balls faced
                - fours: Number of fours
                - sixes: Number of sixes
                - is_duck: Boolean if player got out for duck
                - is_bowler: Boolean if player is a bowler
        
        Returns:
            Total batting fantasy points
        """
        points = 0.0
        
        # Basic runs
        runs = player_stats.get('runs', 0)
        points += runs * self.rules.RUN
        
        # Boundaries
        fours = player_stats.get('fours', 0)
        sixes = player_stats.get('sixes', 0)
        points += fours * self.rules.FOUR
        points += sixes * self.rules.SIX
        
        # Duck penalty (excluding bowlers)
        if player_stats.get('is_duck', False) and not player_stats.get('is_bowler', False):
            points += self.rules.DUCK
        
        # Milestone bonuses
        if runs >= 25:
            points += self.rules.RUNS_25
        if runs >= 50:
            points += self.rules.RUNS_50
        if runs >= 75:
            points += self.rules.RUNS_75
        if runs >= 100:
            points += self.rules.RUNS_100
        if runs >= 125:
            points += self.rules.RUNS_125
        
        # Strike rate bonus (minimum 6 balls)
        balls_faced = player_stats.get('balls_faced', 0)
        if balls_faced >= 6:
            strike_rate = (runs / balls_faced) * 100
            sr_bonus = self._get_strike_rate_bonus(strike_rate)
            points += sr_bonus
        
        return points
    
    def calculate_bowling_points(self, player_stats: Dict) -> float:
        """
        Calculate bowling fantasy points for a player
        
        Args:
            player_stats: Dictionary containing bowling statistics
                - wickets: Total wickets taken
                - overs: Overs bowled
                - runs_conceded: Runs conceded
                - maidens: Maiden overs
                - dots: Dot balls
                - lbw_bowled: LBW/Bowled wickets
        
        Returns:
            Total bowling fantasy points
        """
        points = 0.0
        
        # Wickets
        wickets = player_stats.get('wickets', 0)
        points += wickets * self.rules.WICKET
        
        # Maidens
        maidens = player_stats.get('maidens', 0)
        points += maidens * self.rules.MAIDEN
        
        # Dot balls
        dots = player_stats.get('dots', 0)
        points += dots * self.rules.DOT_BALL
        
        # LBW/Bowled bonus
        lbw_bowled = player_stats.get('lbw_bowled', 0)
        points += lbw_bowled * self.rules.LBW_BOWLED_BONUS
        
        # Wicket milestones
        if wickets >= 3:
            points += self.rules.WICKETS_3
        if wickets >= 4:
            points += self.rules.WICKETS_4
        if wickets >= 5:
            points += self.rules.WICKETS_5
        if wickets >= 6:
            points += self.rules.WICKETS_6
        
        # Economy rate bonus (minimum 1 over)
        overs = player_stats.get('overs', 0)
        if overs >= 1:
            runs_conceded = player_stats.get('runs_conceded', 0)
            economy = runs_conceded / overs
            economy_bonus = self._get_economy_bonus(economy)
            points += economy_bonus
        
        return points
    
    def calculate_fielding_points(self, player_stats: Dict) -> float:
        """
        Calculate fielding fantasy points for a player
        
        Args:
            player_stats: Dictionary containing fielding statistics
                - catches: Number of catches
                - stumpings: Number of stumpings
                - runout_direct: Direct hit runouts
                - runout_involved: Runouts involved in
        
        Returns:
            Total fielding fantasy points
        """
        points = 0.0
        
        # Catches
        catches = player_stats.get('catches', 0)
        points += catches * self.rules.CATCH
        
        # Stumpings
        stumpings = player_stats.get('stumpings', 0)
        points += stumpings * self.rules.STUMPING
        
        # Runouts
        runout_direct = player_stats.get('runout_direct', 0)
        runout_involved = player_stats.get('runout_involved', 0)
        points += runout_direct * self.rules.RUNOUT_DIRECT
        points += runout_involved * self.rules.RUNOUT_EACH
        
        return points
    
    def calculate_bonus_points(self, player_stats: Dict) -> float:
        """
        Calculate bonus fantasy points
        
        Args:
            player_stats: Dictionary containing bonus information
                - starting_xi: Boolean
                - impact_player: Boolean
                - winning_team: Boolean
                - man_of_match: Boolean
        
        Returns:
            Total bonus fantasy points
        """
        points = 0.0
        
        if player_stats.get('starting_xi', False):
            points += self.rules.STARTING_XI
        
        if player_stats.get('impact_player', False):
            points += self.rules.IMPACT_PLAYER
        
        if player_stats.get('winning_team', False):
            points += self.rules.WINNING_TEAM
        
        if player_stats.get('man_of_match', False):
            points += self.rules.MAN_OF_MATCH
        
        return points
    
    def calculate_total_points(self, player_stats: Dict, 
                              is_captain: bool = False, 
                              is_vice_captain: bool = False) -> float:
        """
        Calculate total fantasy points for a player
        
        Args:
            player_stats: Complete player statistics dictionary
            is_captain: Whether player is captain
            is_vice_captain: Whether player is vice captain
        
        Returns:
            Total fantasy points with multipliers applied
        """
        batting_points = self.calculate_batting_points(player_stats)
        bowling_points = self.calculate_bowling_points(player_stats)
        fielding_points = self.calculate_fielding_points(player_stats)
        bonus_points = self.calculate_bonus_points(player_stats)
        
        total = batting_points + bowling_points + fielding_points + bonus_points
        
        # Apply multipliers
        if is_captain:
            total *= self.rules.CAPTAIN_MULTIPLIER
        elif is_vice_captain:
            total *= self.rules.VICE_CAPTAIN_MULTIPLIER
        
        return total
    
    def _get_strike_rate_bonus(self, strike_rate: float) -> int:
        """Get strike rate bonus based on SR value"""
        for (lower, upper), bonus in self.rules.SR_BONUS.items():
            if lower <= strike_rate <= upper:
                return bonus
        return 0
    
    def _get_economy_bonus(self, economy: float) -> int:
        """Get economy rate bonus based on economy value"""
        for (lower, upper), bonus in self.rules.ECONOMY_BONUS.items():
            if lower <= economy <= upper:
                return bonus
        return 0
    
    def process_match_data(self, match_data: Dict) -> pd.DataFrame:
        """
        Process complete match data and calculate fantasy points for all players
        
        Args:
            match_data: Complete match data from JSON
        
        Returns:
            DataFrame with player-wise fantasy points
        """
        player_points = []
        
        # Extract player statistics from match data
        player_stats = self._extract_player_stats(match_data)
        
        for player_name, stats in player_stats.items():
            points = self.calculate_total_points(stats)
            
            player_points.append({
                'player_name': player_name,
                'match_id': match_data.get('info', {}).get('event', {}).get('match_number'),
                'batting_points': self.calculate_batting_points(stats),
                'bowling_points': self.calculate_bowling_points(stats),
                'fielding_points': self.calculate_fielding_points(stats),
                'bonus_points': self.calculate_bonus_points(stats),
                'total_points': points,
                'runs': stats.get('runs', 0),
                'wickets': stats.get('wickets', 0),
                'catches': stats.get('catches', 0)
            })
        
        return pd.DataFrame(player_points)
    
    def _extract_player_stats(self, match_data: Dict) -> Dict:
        """
        Extract player statistics from ball-by-ball match data
        
        Args:
            match_data: Complete match JSON data
        
        Returns:
            Dictionary of player statistics
        """
        player_stats = {}
        
        # Get match info
        info = match_data.get('info', {})
        winner = info.get('outcome', {}).get('winner', '')
        player_of_match = info.get('player_of_match', [])
        
        # Initialize all players
        for team, players in info.get('players', {}).items():
            for player in players:
                player_stats[player] = {
                    'runs': 0,
                    'balls_faced': 0,
                    'fours': 0,
                    'sixes': 0,
                    'is_duck': False,
                    'is_bowler': False,
                    'wickets': 0,
                    'overs': 0,
                    'balls_bowled': 0,
                    'runs_conceded': 0,
                    'maidens': 0,
                    'dots': 0,
                    'lbw_bowled': 0,
                    'catches': 0,
                    'stumpings': 0,
                    'runout_direct': 0,
                    'runout_involved': 0,
                    'starting_xi': True,
                    'impact_player': False,
                    'winning_team': team == winner,
                    'man_of_match': player in player_of_match
                }
        
        # Process innings
        for innings in match_data.get('innings', []):
            for over_data in innings.get('overs', []):
                for delivery in over_data.get('deliveries', []):
                    self._process_delivery(delivery, player_stats)
        
        # Calculate overs and check for ducks
        for player, stats in player_stats.items():
            if stats['balls_bowled'] > 0:
                stats['overs'] = stats['balls_bowled'] / 6
                stats['is_bowler'] = True
            
            if stats['balls_faced'] > 0 and stats['runs'] == 0:
                stats['is_duck'] = True
        
        return player_stats
    
    def _process_delivery(self, delivery: Dict, player_stats: Dict):
        """Process a single delivery and update player stats"""
        batter = delivery.get('batter')
        bowler = delivery.get('bowler')
        runs = delivery.get('runs', {})
        
        # Batting stats
        if batter in player_stats:
            player_stats[batter]['balls_faced'] += 1
            batter_runs = runs.get('batter', 0)
            player_stats[batter]['runs'] += batter_runs
            
            if batter_runs == 4:
                player_stats[batter]['fours'] += 1
            elif batter_runs == 6:
                player_stats[batter]['sixes'] += 1
        
        # Bowling stats
        if bowler in player_stats:
            # Only count legal deliveries
            if 'wides' not in delivery.get('extras', {}) and 'noballs' not in delivery.get('extras', {}):
                player_stats[bowler]['balls_bowled'] += 1
            
            total_runs = runs.get('total', 0)
            player_stats[bowler]['runs_conceded'] += total_runs
            
            if total_runs == 0:
                player_stats[bowler]['dots'] += 1
            
            # Wickets
            wickets = delivery.get('wickets', [])
            for wicket in wickets:
                player_stats[bowler]['wickets'] += 1
                
                if wicket.get('kind') in ['lbw', 'bowled']:
                    player_stats[bowler]['lbw_bowled'] += 1
                
                # Fielding credits
                if wicket.get('kind') == 'caught':
                    fielders = wicket.get('fielders', [])
                    for fielder in fielders:
                        fielder_name = fielder.get('name')
                        if fielder_name in player_stats:
                            player_stats[fielder_name]['catches'] += 1
                
                elif wicket.get('kind') == 'stumped':
                    fielders = wicket.get('fielders', [])
                    for fielder in fielders:
                        fielder_name = fielder.get('name')
                        if fielder_name in player_stats:
                            player_stats[fielder_name]['stumpings'] += 1
                
                elif wicket.get('kind') == 'run out':
                    fielders = wicket.get('fielders', [])
                    for fielder in fielders:
                        fielder_name = fielder.get('name')
                        if fielder_name in player_stats:
                            # Simplified: treat all runouts as involved
                            player_stats[fielder_name]['runout_involved'] += 1
