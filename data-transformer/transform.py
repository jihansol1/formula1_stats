import pandas as pd
import os

SEASON = 2024

def load_kaggle_data():
    """Load all CSV files from Kaggle dataset"""
    data_path = 'data/kaggle/'

    return {
        'circuits': pd.read_csv(f'{data_path}circuits.csv'),
        'constructors': pd.read_csv(f'{data_path}constructors.csv'),
        'drivers': pd.read_csv(f'{data_path}drivers.csv'),
        'races': pd.read_csv(f'{data_path}races.csv'),
        'results': pd.read_csv(f'{data_path}results.csv'),
        'sprint_results': pd.read_csv(f'{data_path}sprint_results.csv'),
        'qualifying': pd.read_csv(f'{data_path}qualifying.csv'),
        'status': pd.read_csv(f'{data_path}status.csv')
    }

def create_races_table(data, season):
    """Create races table for specified season"""
    races = data['races'].merge(data['circuits'], on='circuitId')
    races = races[races['year'] == season]

    output = pd.DataFrame({
        'race_id': races['raceId'],
        'name': races['name_x'],
        'circuit': races['name_y'],
        'country': races['country'],
        'date': races['date'],
        'season': races['year']
    })

    return output.sort_values('date')

def get_combined_points(data, season):
    """Combine race results and sprint results for accurate points"""
    # Get race IDs for the season
    season_races = data['races'][data['races']['year'] == season]['raceId'].tolist()

    # Filter race results for season
    race_results = data['results'][data['results']['raceId'].isin(season_races)].copy()
    race_results['result_type'] = 'race'

    # Filter sprint results for season
    sprint_results = data['sprint_results'][data['sprint_results']['raceId'].isin(season_races)].copy()
    sprint_results['result_type'] = 'sprint'

    print(f"  Found {len(race_results)} race results")
    print(f"  Found {len(sprint_results)} sprint results")

    return race_results, sprint_results

def create_teams_table(data, season):
    """Create teams table with combined race + sprint stats"""
    race_results, sprint_results = get_combined_points(data, season)

    # Aggregate race results
    race_stats = race_results.groupby('constructorId').agg({
        'points': 'sum',
        'positionOrder': lambda x: (x == 1).sum(),
    }).reset_index()
    race_stats.columns = ['constructorId', 'race_points', 'race_wins']

    # Aggregate sprint results
    sprint_stats = sprint_results.groupby('constructorId').agg({
        'points': 'sum',
        'positionOrder': lambda x: (x == 1).sum(),
    }).reset_index()
    sprint_stats.columns = ['constructorId', 'sprint_points', 'sprint_wins']

    # Combine
    team_stats = race_stats.merge(sprint_stats, on='constructorId', how='left')
    team_stats['sprint_points'] = team_stats['sprint_points'].fillna(0)
    team_stats['sprint_wins'] = team_stats['sprint_wins'].fillna(0)

    team_stats['points'] = team_stats['race_points'] + team_stats['sprint_points']
    team_stats['wins'] = team_stats['race_wins']  # Only count main race wins

    # Count podiums (race only)
    podiums = race_results[race_results['positionOrder'] <= 3].groupby('constructorId').size().reset_index(name='podiums')
    team_stats = team_stats.merge(podiums, on='constructorId', how='left')
    team_stats['podiums'] = team_stats['podiums'].fillna(0).astype(int)

    # Add team info
    teams = team_stats.merge(data['constructors'], on='constructorId')

    output = pd.DataFrame({
        'team_id': teams['constructorRef'],
        'name': teams['name'],
        'nationality': teams['nationality'],
        'points': teams['points'].astype(int),
        'wins': teams['wins'].astype(int),
        'podiums': teams['podiums'].astype(int)
    })

    return output

def create_drivers_table(data, season):
    """Create drivers table with combined race + sprint stats"""
    race_results, sprint_results = get_combined_points(data, season)

    # Aggregate race results
    race_stats = race_results.groupby('driverId').agg({
        'points': 'sum',
        'positionOrder': lambda x: (x == 1).sum(),
        'grid': lambda x: (x == 1).sum()
    }).reset_index()
    race_stats.columns = ['driverId', 'race_points', 'race_wins', 'poles']

    # Aggregate sprint results
    sprint_stats = sprint_results.groupby('driverId').agg({
        'points': 'sum',
    }).reset_index()
    sprint_stats.columns = ['driverId', 'sprint_points']

    # Combine
    driver_stats = race_stats.merge(sprint_stats, on='driverId', how='left')
    driver_stats['sprint_points'] = driver_stats['sprint_points'].fillna(0)

    driver_stats['points'] = driver_stats['race_points'] + driver_stats['sprint_points']
    driver_stats['wins'] = driver_stats['race_wins']  # Only count main race wins

    # Count podiums (race only)
    podiums = race_results[race_results['positionOrder'] <= 3].groupby('driverId').size().reset_index(name='podiums')
    driver_stats = driver_stats.merge(podiums, on='driverId', how='left')
    driver_stats['podiums'] = driver_stats['podiums'].fillna(0).astype(int)

    # Get current team
    latest_race = race_results.sort_values('raceId').groupby('driverId').last().reset_index()
    driver_teams = latest_race[['driverId', 'constructorId']]

    driver_stats = driver_stats.merge(driver_teams, on='driverId')
    driver_stats = driver_stats.merge(data['drivers'], on='driverId')
    driver_stats = driver_stats.merge(data['constructors'][['constructorId', 'constructorRef']], on='constructorId')

    output = pd.DataFrame({
        'driver_id': driver_stats['driverRef'],
        'name': driver_stats['forename'] + ' ' + driver_stats['surname'],
        'team_id': driver_stats['constructorRef'],
        'nationality': driver_stats['nationality'],
        'number': driver_stats['number'],
        'points': driver_stats['points'].astype(int),
        'wins': driver_stats['wins'].astype(int),
        'podiums': driver_stats['podiums'].astype(int),
        'poles': driver_stats['poles'].astype(int)
    })

    return output

def create_results_table(data, season):
    """Create results table combining race and sprint results"""
    race_results, sprint_results = get_combined_points(data, season)

    # Process race results
    race_df = race_results.merge(data['drivers'], on='driverId')
    race_df = race_df.merge(data['status'], on='statusId')

    race_output = pd.DataFrame({
        'result_id': race_df['resultId'],
        'race_id': race_df['raceId'],
        'driver_id': race_df['driverRef'],
        'position': race_df['positionOrder'],
        'points': race_df['points'].astype(int),
        'grid_position': race_df['grid'],
        'status': race_df['status'],
        'fastest_lap': race_df['fastestLapTime'],
        'is_sprint': 'false'
    })

    # Process sprint results
    sprint_df = sprint_results.merge(data['drivers'], on='driverId')
    sprint_df = sprint_df.merge(data['status'], on='statusId')

    # Generate unique result_ids for sprints (offset to avoid collision)
    max_result_id = race_output['result_id'].max()
    sprint_output = pd.DataFrame({
        'result_id': range(max_result_id + 1, max_result_id + 1 + len(sprint_df)),
        'race_id': sprint_df['raceId'],
        'driver_id': sprint_df['driverRef'],
        'position': sprint_df['positionOrder'],
        'points': sprint_df['points'].astype(int),
        'grid_position': sprint_df['grid'],
        'status': sprint_df['status'],
        'fastest_lap': sprint_df['fastestLapTime'],
        'is_sprint': 'true'
    })

    # Combine both
    output = pd.concat([race_output, sprint_output], ignore_index=True)
    output = output.sort_values(['race_id', 'is_sprint', 'position'])

    return output

def create_qualifying_table(data, season):
    """Create qualifying table for specified season"""
    season_races = data['races'][data['races']['year'] == season]['raceId'].tolist()

    qualifying = data['qualifying'][data['qualifying']['raceId'].isin(season_races)]
    qualifying = qualifying.merge(data['drivers'], on='driverId')

    output = pd.DataFrame({
        'qualifying_id': qualifying['qualifyId'],
        'race_id': qualifying['raceId'],
        'driver_id': qualifying['driverRef'],
        'position': qualifying['position'],
        'q1_time': qualifying['q1'],
        'q2_time': qualifying['q2'],
        'q3_time': qualifying['q3']
    })

    return output

def main():
    print(f"Loading Kaggle data...")
    data = load_kaggle_data()

    print(f"\nProcessing {SEASON} season (with sprint races)...")

    # Create output directory
    os.makedirs('output', exist_ok=True)

    # Generate tables
    print("\nCreating races table...")
    races = create_races_table(data, SEASON)
    races.to_csv('output/races.csv', index=False)
    print(f"  → {len(races)} races")

    print("\nCreating teams table...")
    teams = create_teams_table(data, SEASON)
    teams.to_csv('output/teams.csv', index=False)
    print(f"  → {len(teams)} teams")

    print("\nCreating drivers table...")
    drivers = create_drivers_table(data, SEASON)
    drivers.to_csv('output/drivers.csv', index=False)
    print(f"  → {len(drivers)} drivers")

    print("\nCreating results table (race + sprint)...")
    results = create_results_table(data, SEASON)
    results.to_csv('output/results.csv', index=False)
    print(f"  → {len(results)} total results ({len(results[results['is_sprint']==False])} race, {len(results[results['is_sprint']==True])} sprint)")

    print("\nCreating qualifying table...")
    qualifying = create_qualifying_table(data, SEASON)
    qualifying.to_csv('output/qualifying.csv', index=False)
    print(f"  → {len(qualifying)} qualifying records")

    # Verify top drivers
    print("\n--- Verification: Top 5 Drivers ---")
    top_drivers = drivers.nlargest(5, 'points')[['name', 'points', 'wins']]
    print(top_drivers.to_string(index=False))

    print("\n--- Verification: Top 5 Teams ---")
    top_teams = teams.nlargest(5, 'points')[['name', 'points', 'wins']]
    print(top_teams.to_string(index=False))

    print("\nDone! Files saved to output/")

if __name__ == '__main__':
    main()