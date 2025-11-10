import pandas as pd
import numpy as np

CURRENT_GRID = ['NOR', 'LEC', 'HAM', 'RUS', 'VER', 'ANT', 'SAI', 'PIA', 'HAD', 'BEA',
                'TSU', 'OCO', 'HUL', 'ALO', 'LAW', 'BOR', 'ALB', 'GAS', 'STR', 'COL']

def get_next_race(data_df, grid = False):
    next_race = data_df.iloc[-20:, :].copy()
    if next_race['raceID'].iloc[0] < 24: # Hardcoded length for 2025, will change it for a getter function later
        numeric_columns = [
            'avgLapTime_s', 'stdLapTime_s', 'Position', 'isDNF', 'perRaceMinAvgLapTime',
            'BadResult', 'perRace_Team_Avg_Pos', 'gridAdjustedPace'
            ]
        
        next_race[numeric_columns] = np.nan

        next_race['raceID'] += 1
        next_race['isPredictionData'] = 1
        if grid:
            grid_map = {driver_name: i + 1 for i, driver_name in enumerate(CURRENT_GRID)}
            next_race['GridPosition'] = next_race['Driver'].map(grid_map)
            return next_race
    
    return next_race

def pred_cols(grid = False):
    if grid:
        cols = [
            # Expanding Averages
            'Prev_Avg_avgLapTime_s_norm', 'Prev_Avg_stdLapTime_s_norm', 'Prev_Avg_GridPosition',
            'Prev_Avg_Position',
            # Per Track Expanding Averages
            'Prev_Avg_Finish_Track', 'Prev_Avg_Quali_Track',
            # Per Team Expanding Averages
            'Prev_Avg_TeamPace', 'Prev_Avg_TeamFQualiPos',
            # Rolling Averages
            'Rolling_Prev_Avg_avgLapTime_s_norm', 'Rolling_Prev_Avg_stdLapTime_s_norm',
            'Rolling_Prev_Avg_GridPosition', 'Rolling_Prev_Avg_Position',
            # Per Track Rolling Averages
            'Rolling_Prev_Avg_Finish_Track', 'Rolling_Prev_Avg_Quali_Track',
            # Per Team Rolling Averages
            'Rolling_Prev_Avg_TeamPace', 'Rolling_Prev_Avg_TeamFQualiPos',
            # New Feature, Grid Adjusted Pace
            'gridAdjustedPace',
            # Grid = True
            'GridPosition'
         ]
        return cols

    cols = [
        # Expanding Averages
        'Prev_Avg_avgLapTime_s_norm', 'Prev_Avg_stdLapTime_s_norm', 'Prev_Avg_GridPosition',
        'Prev_Avg_Position',
        # Per Track Expanding Averages
        'Prev_Avg_Finish_Track', 'Prev_Avg_Quali_Track',
        # Per Team Expanding Averages
        'Prev_Avg_TeamPace', 'Prev_Avg_TeamFQualiPos',
        # Rolling Averages
        'Rolling_Prev_Avg_avgLapTime_s_norm', 'Rolling_Prev_Avg_stdLapTime_s_norm',
        'Rolling_Prev_Avg_GridPosition', 'Rolling_Prev_Avg_Position',
        # Per Track Rolling Averages
        'Rolling_Prev_Avg_Finish_Track', 'Rolling_Prev_Avg_Quali_Track',
        # Per Team Rolling Averages
        'Rolling_Prev_Avg_TeamPace', 'Rolling_Prev_Avg_TeamFQualiPos',
        # New Feature, Grid Adjusted Pace
        'gridAdjustedPace'
    ]
    return cols

# IMPORTANT :
# MAKE GETTERS FOR raceID and CircuitName