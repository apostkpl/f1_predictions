import pandas as pd

# Window Size, to be used in the functions that calculate the rolling historical averages
WINDOW_SIZE = 5 # MAY NEED CHANGE

# Rolling Averages for avg lap time, std lap time, grid position and final position
def basic_rolling_averages(raw_data):
    # Calculate the best (minimum) average Pace for each circuit, regardless of Driver,
    # but up to (but EXCLUDING, using .shift(1)) the CURRENT race
    raw_data['perRaceBestAvgLapTime'] = raw_data.groupby('CircuitName')['avgLapTime_s'].transform(
        lambda x: x.expanding(min_periods = 1).min().shift(1)
    )

    # Normalize the average lap time column (This is a column that comes directly from our f1_downloader.py)
    raw_data['avgLapTime_s_norm'] = (
        (raw_data['avgLapTime_s'] - raw_data['perRaceBestAvgLapTime']) / raw_data['perRaceBestAvgLapTime']
        )
    # Calculate the normalized standard deviation
    raw_data['stdLapTime_s_norm'] = (raw_data['stdLapTime_s'] / raw_data['perRaceBestAvgLapTime'])

    # Columns we want to calculate the historical mean for:
    target_cols = ['avgLapTime_s_norm', 'stdLapTime_s_norm', 'GridPosition', 'Position']

    for col in target_cols:

        # Group the data by driver:
        driver_stats = raw_data.groupby('Driver')[col]

        # Calculate the expanding mean up to the previous race:
        raw_data[f'Prev_Avg_{col}'] = driver_stats.transform(
        # Calculate the expanding mean. Shift one position to the left so that we do not include the current race
        # to the predictors table (X) and avoid data leakage. We use Pandas' .shift(1) for that.
            lambda x: x.expanding(min_periods = 1).mean().shift(1)
        )

        # Calculate the rolling mean (for a given window of races) up to the previous race:
        raw_data[f'Rolling_Prev_Avg_{col}'] = driver_stats.transform(
        # Calculate the rolling mean. Shift one position to the left so that we do not include the current race
        # to the predictors table (X) and avoid data leakage. We use Pandas' .shift(1) for that.
        lambda x: x.rolling(window = WINDOW_SIZE, min_periods = 1).mean().shift(1)
        )
    

# Additional rolling averages, grouped by race
def perRace_rolling_averages(raw_data):
    raw_data['Prev_Avg_Finish_Track'] = raw_data.groupby(['Driver', 'CircuitName'])['Position'].transform(
        lambda x: x.expanding(min_periods = 1).mean().shift(1)
    )

    raw_data['Rolling_Prev_Avg_Finish_Track'] = raw_data.groupby(['Driver', 'CircuitName'])['Position'].transform(
        lambda x: x.rolling(window = WINDOW_SIZE, min_periods = 1).mean().shift(1)
    )

    raw_data['Prev_Avg_Quali_Track'] = raw_data.groupby(['Driver', 'CircuitName'])['GridPosition'].transform(
        lambda x: x.expanding(min_periods = 1).mean().shift(1)
    )

    raw_data['Rolling_Prev_Avg_Quali_Track'] = raw_data.groupby(['Driver', 'CircuitName'])['GridPosition'].transform(
        lambda x: x.rolling(window = WINDOW_SIZE, min_periods = 1).mean().shift(1)
    )


# Additional rolling averages, grouped by team
def perTeam_rolling_averages(raw_data):
    # Find out how the team as a whole is doing in recent races when it comes to average lap times
    raw_data['Rolling_Prev_Avg_TeamPace'] = raw_data.groupby('Team')['avgLapTime_s_norm'].transform(
        lambda x: x.rolling(window = WINDOW_SIZE, min_periods = 1).mean().shift(1)
    )

    raw_data['Prev_Avg_TeamPace'] = raw_data.groupby('Team')['avgLapTime_s_norm'].transform(
        lambda x: x.expanding(min_periods = 1).mean().shift(1)
    )
    
    raw_data['Rolling_Prev_Avg_TeamFQualiPos'] = raw_data.groupby('Team')['GridPosition'].transform(
        lambda x: x.rolling(window = WINDOW_SIZE, min_periods = 1).mean().shift(1)
    )

    raw_data['Prev_Avg_TeamFQualiPos'] = raw_data.groupby('Team')['GridPosition'].transform(
        lambda x: x.expanding(min_periods = 1).mean().shift(1)
    )


# Rolling DNFs
def perDriver_rolling_dnf(raw_data):
    raw_data['Rolling_Prev_DNF_Status'] = raw_data.groupby('Driver')['isDNF'].transform(
        lambda x: x.rolling(window = WINDOW_SIZE, min_periods = 1).sum().shift(1)
    )
    # Fill NA with zeros, aka not DNF
    raw_data['Rolling_Prev_DNF_Status'] = raw_data['Rolling_Prev_DNF_Status'].fillna(0)

    # EXTRA
    # Penalize bad results
    raw_data['BadResult'] = (raw_data['Position'] > 10).astype(int)
    raw_data['Rolling_Prev_BadResult'] = raw_data.groupby('Driver')['BadResult'].transform(
        lambda x: x.rolling(window = WINDOW_SIZE, min_periods = 1).sum().shift(1)
        )

# !!! FOR TESTING PURPOSES !!! SEE IF THE MODEL PERFORMS BETTER WITH A PACE METRIC ADJUSTED TO GRID POSITION
# The goal is to make the current grid position matter more. <TEST NEEDED>
def grid_adjusted_pace(raw_data):
    raw_data['gridAdjustedPace'] = (
        raw_data['Rolling_Prev_Avg_avgLapTime_s_norm'] * raw_data['Rolling_Prev_Avg_GridPosition']
    )


# Helper function to gather all historical data
# This function will in-place actions to our dataframe
def collect_historical_data(raw_data):
    # Call all rolling functions
    basic_rolling_averages(raw_data)
    perRace_rolling_averages(raw_data)
    perTeam_rolling_averages(raw_data)
    perDriver_rolling_dnf(raw_data)
    # New currently in TESTING
    grid_adjusted_pace(raw_data)


def drop_na(data_df): # IMPORTAND, collect_historical_data() must run BEFORE this one
    data_df.dropna(
        subset = [
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
        ],
        inplace = True
        )

