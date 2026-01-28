# F1 Stats Dashboard 🏎️

A full-stack Formula 1 statistics application featuring dynamic championship standings visualization across multiple seasons (2018-2024). Select any Grand Prix from an interactive timeline to see driver and constructor standings as they were at that point in the season.

## Features

- **Multi-Season Support**: Browse championship standings from 2018-2024 (7 seasons, 150+ races)
- **Dynamic Standings Timeline**: View standings as they were after any race in any season
- **Sprint Race Integration**: Includes sprint race points for accurate championship calculations
- **Driver Championship**: Points, wins, and podiums calculated dynamically up to selected race
- **Constructor Championship**: Team standings using historical driver-team mappings (accurate even when drivers change teams)
- **Interactive Race Timeline**: Click any race to instantly recalculate standings
- **Season Selector**: Dropdown to switch between seasons seamlessly

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Java 17, Spring Boot 3.2 |
| Database | PostgreSQL 14 |
| ORM | Spring Data JPA |
| Data Processing | Python 3, Pandas |
| Frontend | React 18, Axios |

## Project Structure
```
f1stats/
├── src/main/java/com/sol/f1stats/
│   ├── F1StatsApplication.java
│   ├── config/
│   │   └── CorsConfig.java
│   ├── controller/
│   │   ├── RaceController.java
│   │   └── StandingsController.java
│   ├── service/
│   │   └── StandingsService.java
│   ├── repository/
│   │   ├── DriverRepository.java
│   │   ├── TeamRepository.java
│   │   ├── RaceRepository.java
│   │   └── ResultRepository.java
│   ├── model/
│   │   ├── Driver.java
│   │   ├── Team.java
│   │   ├── Race.java
│   │   ├── Result.java
│   │   └── Qualifying.java
│   └── dto/
│       ├── DriverStandingDTO.java
│       └── ConstructorStandingDTO.java
├── frontend/
│   └── src/
│       ├── App.js
│       ├── App.css
│       ├── components/
│       │   ├── Timeline.js
│       │   ├── SeasonSelector.js
│       │   ├── DriverStandings.js
│       │   └── ConstructorStandings.js
│       └── services/
│           └── api.js
├── data-transformer/
│   └── transform.py
└── README.md
```

## Database Schema
```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│   teams     │       │   drivers   │       │    races    │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ team_id (PK)│◄──────│ team_id (FK)│       │ race_id (PK)│
│ name        │       │ driver_id(PK)│       │ name        │
│ nationality │       │ name        │       │ circuit     │
│ points      │       │ nationality │       │ country     │
│ wins        │       │ number      │       │ date        │
│ podiums     │       │ points      │       │ season      │
└─────────────┘       │ wins        │       └──────┬──────┘
                      │ podiums     │              │
                      │ poles       │              │
                      └──────┬──────┘              │
                             │                     │
                             ▼                     ▼
                      ┌─────────────────────────────┐
                      │          results            │
                      ├─────────────────────────────┤
                      │ result_id (PK)              │
                      │ race_id (FK)                │
                      │ driver_id (FK)              │
                      │ constructor_id              │
                      │ position                    │
                      │ points                      │
                      │ grid_position               │
                      │ status                      │
                      │ fastest_lap                 │
                      │ is_sprint                   │
                      └─────────────────────────────┘

┌─────────────┐
│ qualifying  │
├─────────────┤
│ qual_id (PK)│
│ race_id (FK)│
│ driver_id(FK)│
│ position    │
│ q1_time     │
│ q2_time     │
│ q3_time     │
└─────────────┘
```

## API Endpoints

### Races
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/races` | Get all races ordered by date |
| GET | `/api/races/{raceId}` | Get specific race details |
| GET | `/api/races/season/{season}` | Get all races for a season |

### Standings
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/standings/drivers?upToRaceId={id}` | Driver standings up to specified race |
| GET | `/api/standings/constructors?upToRaceId={id}` | Constructor standings up to specified race |

### Example Response

**GET** `/api/standings/drivers?upToRaceId=1144` (2024 Abu Dhabi GP)
```json
[
  {
    "position": 1,
    "driverId": "max_verstappen",
    "name": "Max Verstappen",
    "teamId": "red_bull",
    "points": 437,
    "wins": 9,
    "podiums": 14
  },
  {
    "position": 2,
    "driverId": "norris",
    "name": "Lando Norris",
    "teamId": "mclaren",
    "points": 374,
    "wins": 4,
    "podiums": 13
  }
]
```

## Getting Started

### Prerequisites

- Java 17+
- PostgreSQL 14+
- Python 3.9+
- Node.js 18+
- Maven

### 1. Clone the Repository
```bash
git clone https://github.com/jihansol1/f1stats.git
cd f1stats
```

### 2. Database Setup

Start PostgreSQL:
```bash
brew services start postgresql@14
```

Create tables:
```sql
CREATE TABLE teams (
    team_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    nationality VARCHAR(50),
    points INTEGER,
    wins INTEGER,
    podiums INTEGER
);

CREATE TABLE races (
    race_id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    circuit VARCHAR(100),
    country VARCHAR(50),
    date DATE,
    season INTEGER
);

CREATE TABLE drivers (
    driver_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    team_id VARCHAR(50) REFERENCES teams(team_id),
    nationality VARCHAR(50),
    number INTEGER,
    points INTEGER,
    wins INTEGER,
    podiums INTEGER,
    poles INTEGER
);

CREATE TABLE results (
    result_id INTEGER PRIMARY KEY,
    race_id INTEGER REFERENCES races(race_id),
    driver_id VARCHAR(50) REFERENCES drivers(driver_id),
    constructor_id VARCHAR(50),
    position INTEGER,
    points INTEGER,
    grid_position INTEGER,
    status VARCHAR(50),
    fastest_lap VARCHAR(20),
    is_sprint BOOLEAN DEFAULT FALSE
);

CREATE TABLE qualifying (
    qualifying_id INTEGER PRIMARY KEY,
    race_id INTEGER REFERENCES races(race_id),
    driver_id VARCHAR(50) REFERENCES drivers(driver_id),
    position INTEGER,
    q1_time VARCHAR(20),
    q2_time VARCHAR(20),
    q3_time VARCHAR(20)
);
```

### 3. Run the Data Pipeline
```bash
cd data-transformer
python3 -m venv venv
source venv/bin/activate
pip install pandas
python transform.py
```

Load data into PostgreSQL:
```bash
psql postgres

COPY teams FROM '/path/to/output/teams.csv' DELIMITER ',' CSV HEADER;
COPY races FROM '/path/to/output/races.csv' DELIMITER ',' CSV HEADER;
COPY drivers FROM '/path/to/output/drivers.csv' DELIMITER ',' CSV HEADER;
COPY results FROM '/path/to/output/results.csv' DELIMITER ',' CSV HEADER;
COPY qualifying FROM '/path/to/output/qualifying.csv' DELIMITER ',' CSV HEADER;
```

### 4. Start the Backend
```bash
./mvnw spring-boot:run
```

The API will be available at `http://localhost:8080`

### 5. Start the Frontend
```bash
cd frontend
npm install
npm start
```

The app will be available at `http://localhost:3000`

## Data Source

- Historical F1 data (1950-2024): [Kaggle - Formula 1 World Championship](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020)
- Includes race results, sprint results, qualifying, driver and constructor information

## Roadmap

- [x] Data transformation pipeline (Python/Pandas)
- [x] PostgreSQL schema design with 5 relational tables
- [x] Spring Boot REST API with dynamic standings calculation
- [x] React frontend with interactive timeline
- [x] Season selector for multi-year support (2018-2024)
- [x] Sprint race points integration
- [x] Constructor standings with historical team mappings
- [ ] Add 2025 season data
- [ ] Race results detail page
- [ ] Driver profile pages
- [ ] Qualifying results view
- [ ] AWS deployment (EC2 + RDS)

## Author

Hansol Ji - [GitHub](https://github.com/jihansol1)