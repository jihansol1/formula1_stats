import pandas as pd
from pathlib import Path

# === CONFIGURATION ===
KAGGLE_DATA_PATH = Path('data/kaggle')
OUTPUT_PATH = Path('output')
SEASON = 2024  # Change this to process different seasons

# Create output directory if it doesn't exist
OUTPUT_PATH.mkdir(exist_ok=True)


def load_kaggle_data():
    """Load all required Kaggle CSV files."""
    print("Loading Kaggle data...")

    data = {
        'circuits': pd.read_csv(KAGGLE_DATA_PATH / 'circuits.csv'),
        'constructors': pd.read_csv(KAGGLE_DATA_PATH / 'constructors.csv'),
        'drivers': pd.read_csv(KAGGLE_DATA_PATH / 'drivers.csv'),
        'races': pd.read_csv(KAGGLE_DATA_PATH / 'races.csv'),
        'results': pd.read_csv(KAGGLE_DATA_PATH / 'results.csv'),
        'qualifying': pd.read_csv(KAGGLE_DATA_PATH / 'qualifying.csv'),
        'status': pd.read_csv(KAGGLE_DATA_PATH / 'status.csv'),
    }

    for name, df in data.items():
        print(f"  Loaded {name}: {len(df)} rows")

    return data


def create_races_table(data: dict, season: int) -> pd.DataFrame:
    """
    Create races table.
    Schema: race_id, name, circuit, country, date, season
    """
    print(f"\nCreating races table for {season}...")

    races = data['races']
    circuits = data['circuits']

    # Filter for the specified season
    season_races = races[races['year'] == season].copy()

    # Join with circuits to get circuit name and country
    merged = season_races.merge(
        circuits[['circuitId', 'name', 'country']],
        on='circuitId',
        suffixes=('', '_circuit')
    )

    # Create output dataframe
    result = pd.DataFrame({
        'race_id': merged['raceId'],
        'name': merged['name'],  # GP name
        'circuit': merged['name_circuit'],  # Circuit name
        'country': merged['country'],
        'date': merged['date'],
        'season': merged['year']
    })

    # Sort by date
    result = result.sort_values('date').reset_index(drop=True)

    print(f"  Created {len(result)} race records")
    return result


def create_teams_table(data: dict, season: int) -> pd.DataFrame:
    """
    Create teams table with calculated stats.
    Schema: team_id, name, nationality, points, wins, podiums
    """
    print(f"\nCreating teams table for {season}...")

    constructors = data['constructors']
    results = data['results']
    races = data['races']

    # Get race IDs for the season
    season_race_ids = races[races['year'] == season]['raceId'].tolist()

    # Filter results for the season
    season_results = results[results['raceId'].isin(season_race_ids)].copy()

    # Get unique constructors that participated this season
    season_constructor_ids = season_results['constructorId'].unique()
    season_constructors = constructors[constructors['constructorId'].isin(season_constructor_ids)].copy()

    # Calculate stats per constructor
    stats = season_results.groupby('constructorId').agg(
        points=('points', 'sum'),
        wins=('positionOrder', lambda x: (x == 1).sum()),
        podiums=('positionOrder', lambda x: (x <= 3).sum())
    ).reset_index()

    # Merge with constructor info
    merged = season_constructors.merge(stats, on='constructorId', how='left')

    # Create output dataframe
    result = pd.DataFrame({
        'team_id': merged['constructorRef'],
        'name': merged['name'],
        'nationality': merged['nationality'],
        'points': merged['points'].fillna(0).astype(int),
        'wins': merged['wins'].fillna(0).astype(int),
        'podiums': merged['podiums'].fillna(0).astype(int)
    })

    # Sort by points descending
    result = result.sort_values('points', ascending=False).reset_index(drop=True)

    print(f"  Created {len(result)} team records")
    return result


def create_drivers_table(data: dict, season: int) -> pd.DataFrame:
    """
    Create drivers table with calculated stats.
    Schema: driver_id, name, team_id, nationality, number, points, wins, podiums, poles
    """
    print(f"\nCreating drivers table for {season}...")

    drivers = data['drivers']
    constructors = data['constructors']
    results = data['results']
    qualifying = data['qualifying']
    races = data['races']

    # Get race IDs for the season
    season_race_ids = races[races['year'] == season]['raceId'].tolist()

    # Filter results for the season
    season_results = results[results['raceId'].isin(season_race_ids)].copy()
    season_qualifying = qualifying[qualifying['raceId'].isin(season_race_ids)].copy()

    # Get unique drivers that participated this season
    season_driver_ids = season_results['driverId'].unique()
    season_drivers = drivers[drivers['driverId'].isin(season_driver_ids)].copy()

    # Calculate race stats per driver
    race_stats = season_results.groupby('driverId').agg(
        points=('points', 'sum'),
        wins=('positionOrder', lambda x: (x == 1).sum()),
        podiums=('positionOrder', lambda x: (x <= 3).sum())
    ).reset_index()

    # Calculate poles per driver
    pole_stats = season_qualifying.groupby('driverId').agg(
        poles=('position', lambda x: (x == 1).sum())
    ).reset_index()

    # Get most recent team for each driver (last race of season)
    last_race_id = season_results['raceId'].max()
    last_race_results = season_results[season_results['raceId'] == last_race_id][['driverId', 'constructorId']]

    # For drivers not in last race, get their most recent race
    drivers_in_last = last_race_results['driverId'].tolist()
    other_drivers = season_results[~season_results['driverId'].isin(drivers_in_last)]
    other_drivers_latest = other_drivers.loc[other_drivers.groupby('driverId')['raceId'].idxmax()][
        ['driverId', 'constructorId']]

    driver_teams = pd.concat([last_race_results, other_drivers_latest])
    driver_teams = driver_teams.merge(constructors[['constructorId', 'constructorRef']], on='constructorId')

    # Merge everything
    merged = season_drivers.merge(race_stats, on='driverId', how='left')
    merged = merged.merge(pole_stats, on='driverId', how='left')
    merged = merged.merge(driver_teams[['driverId', 'constructorRef']], on='driverId', how='left')

    # Create output dataframe
    result = pd.DataFrame({
        'driver_id': merged['driverRef'],
        'name': merged['forename'] + ' ' + merged['surname'],
        'team_id': merged['constructorRef'],
        'nationality': merged['nationality'],
        'number': merged['number'].fillna(0).astype(int),
        'points': merged['points'].fillna(0).astype(int),
        'wins': merged['wins'].fillna(0).astype(int),
        'podiums': merged['podiums'].fillna(0).astype(int),
        'poles': merged['poles'].fillna(0).astype(int)
    })

    # Sort by points descending
    result = result.sort_values('points', ascending=False).reset_index(drop=True)

    print(f"  Created {len(result)} driver records")
    return result


def create_results_table(data: dict, season: int) -> pd.DataFrame:
    """
    Create results table.
    Schema: result_id, race_id, driver_id, position, points, grid_position, status, fastest_lap
    """
    print(f"\nCreating results table for {season}...")

    drivers = data['drivers']
    results = data['results']
    races = data['races']
    status = data['status']

    # Get race IDs for the season
    season_race_ids = races[races['year'] == season]['raceId'].tolist()

    # Filter results for the season
    season_results = results[results['raceId'].isin(season_race_ids)].copy()

    # Join with status to get status text
    merged = season_results.merge(status, on='statusId', how='left')

    # Join with drivers to get driver ref
    merged = merged.merge(drivers[['driverId', 'driverRef']], on='driverId', how='left')

    # Create output dataframe
    result = pd.DataFrame({
        'result_id': merged['resultId'],
        'race_id': merged['raceId'],
        'driver_id': merged['driverRef'],
        'position': merged['positionOrder'],
        'points': merged['points'].astype(int),
        'grid_position': merged['grid'],
        'status': merged['status'],
        'fastest_lap': (merged['rank'] == 1).astype(bool)  # rank 1 = fastest lap
    })

    # Sort by race_id then position
    result = result.sort_values(['race_id', 'position']).reset_index(drop=True)

    print(f"  Created {len(result)} result records")
    return result


def create_qualifying_table(data: dict, season: int) -> pd.DataFrame:
    """
    Create qualifying table.
    Schema: qualifying_id, race_id, driver_id, position, q1_time, q2_time, q3_time
    """
    print(f"\nCreating qualifying table for {season}...")

    drivers = data['drivers']
    qualifying = data['qualifying']
    races = data['races']

    # Get race IDs for the season
    season_race_ids = races[races['year'] == season]['raceId'].tolist()

    # Filter qualifying for the season
    season_qualifying = qualifying[qualifying['raceId'].isin(season_race_ids)].copy()

    # Join with drivers to get driver ref
    merged = season_qualifying.merge(drivers[['driverId', 'driverRef']], on='driverId', how='left')

    # Create output dataframe
    result = pd.DataFrame({
        'qualifying_id': merged['qualifyId'],
        'race_id': merged['raceId'],
        'driver_id': merged['driverRef'],
        'position': merged['position'],
        'q1_time': merged['q1'].replace('\\N', ''),
        'q2_time': merged['q2'].replace('\\N', ''),
        'q3_time': merged['q3'].replace('\\N', '')
    })

    # Sort by race_id then position
    result = result.sort_values(['race_id', 'position']).reset_index(drop=True)

    print(f"  Created {len(result)} qualifying records")
    return result


def main():
    """Main transformation pipeline."""
    print("=" * 50)
    print(f"F1 Data Transformer - Season {SEASON}")
    print("=" * 50)

    # Load data
    data = load_kaggle_data()

    # Create tables
    races = create_races_table(data, SEASON)
    teams = create_teams_table(data, SEASON)
    drivers = create_drivers_table(data, SEASON)
    results = create_results_table(data, SEASON)
    qualifying = create_qualifying_table(data, SEASON)

    # Save to CSV
    print("\nSaving to CSV...")
    races.to_csv(OUTPUT_PATH / 'races.csv', index=False)
    teams.to_csv(OUTPUT_PATH / 'teams.csv', index=False)
    drivers.to_csv(OUTPUT_PATH / 'drivers.csv', index=False)
    results.to_csv(OUTPUT_PATH / 'results.csv', index=False)
    qualifying.to_csv(OUTPUT_PATH / 'qualifying.csv', index=False)

    print("\n" + "=" * 50)
    print("Done! Files saved to output/")
    print("=" * 50)

    # Preview each table
    print("\n--- RACES ---")
    print(races.head())

    print("\n--- TEAMS ---")
    print(teams.head())

    print("\n--- DRIVERS ---")
    print(drivers.head())

    print("\n--- RESULTS (first 10) ---")
    print(results.head(10))

    print("\n--- QUALIFYING (first 10) ---")
    print(qualifying.head(10))


if __name__ == '__main__':
    main()