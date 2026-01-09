# F1 Stats API 🏎️

A full-stack Formula 1 statistics application that provides dynamic championship standings based on any point in the season. Select a Grand Prix from the timeline and see exactly how the Driver and Constructor championships stood at that moment.

## Features

- **Dynamic Standings Timeline**: View championship standings as they were after any race in the season
- **Driver Championship**: Points, wins, podiums calculated dynamically up to selected race
- **Constructor Championship**: Team standings aggregated from driver results
- **Race Calendar**: Full season calendar with circuit and country information
- **RESTful API**: Clean endpoints for integration with any frontend

## Tech Stack

| Layer | Technology               |
|-------|--------------------------|
| Backend | Java 17, Spring Boot 3.2 |
| Database | PostgreSQL 14            |
| ORM | Spring Data JPA          |
| Data Processing | Python 3, Pandas         |
| Frontend | React (coming soon)      |

## Project Structure

```
f1stats/
├── src/main/java/com/sol/f1stats/
│   ├── F1StatsApplication.java
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
├── src/main/resources/
│   └── application.properties
├── data-transformer/           # Python scripts for data processing
│   ├── transform.py
│   ├── data/kaggle/           # Raw Kaggle CSV files
│   └── output/                # Processed CSV files
└── README.md
```

## Database Schema

```
┌─────────────┐       ┌─────────────┐
│   teams     │       │   drivers   │
├─────────────┤       ├─────────────┤
│ team_id (PK)│◄──────│ team_id (FK)│
│ name        │       │ driver_id(PK│
│ nationality │       │ name        │
│ points      │       │ nationality │
│ wins        │       │ number      │
│ podiums     │       │ points      │
└─────────────┘       │ wins        │
                      │ podiums     │
                      │ poles       │
                      └──────┬──────┘
                             │
┌─────────────┐       ┌──────▼──────┐
│   races     │       │   results   │
├─────────────┤       ├─────────────┤
│ race_id (PK)│◄──────│ race_id (FK)│
│ name        │       │ driver_id(FK│
│ circuit     │       │ result_id(PK│
│ country     │       │ position    │
│ date        │       │ points      │
│ season      │       │ grid_position
└─────────────┘       │ status      │
                      │ fastest_lap │
                      └─────────────┘

┌─────────────┐
│ qualifying  │
├─────────────┤
│ qual_id (PK)│
│ race_id (FK)│
│ driver_id(FK│
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

**GET** `/api/standings/drivers?upToRaceId=1130`

```json
[
  {
    "position": 1,
    "driverId": "verstappen",
    "name": "Max Verstappen",
    "teamId": "red_bull",
    "points": 102,
    "wins": 4,
    "podiums": 5
  },
  {
    "position": 2,
    "driverId": "perez",
    "name": "Sergio Pérez",
    "teamId": "red_bull",
    "points": 79,
    "wins": 0,
    "podiums": 3
  }
]
```

## Getting Started

### Prerequisites

- Java 17+
- PostgreSQL 15+
- Python 3.9+ (for data transformation)
- Maven

### Database Setup

1. Create the database:
```sql
CREATE DATABASE f1stats;
```

2. Create tables:
```sql
-- See schema in /docs/schema.sql
```

3. Load data using the Python transformer:
```bash
cd data-transformer
python3 -m venv venv
source venv/bin/activate
pip install pandas
python transform.py
```

4. Import CSVs to PostgreSQL:
```sql
COPY teams FROM '/path/to/output/teams.csv' DELIMITER ',' CSV HEADER;
-- Repeat for other tables
```

### Running the Application

```bash
./mvnw spring-boot:run
```

The API will be available at `http://localhost:8080`

## Data Source

- Historical F1 data (1950-2024): [Kaggle - Formula 1 World Championship](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020)

## Roadmap

- [x] Data transformation pipeline (Python)
- [x] PostgreSQL schema design
- [x] Spring Boot REST API
- [ ] React frontend with timeline component
- [ ] Interactive standings tables
- [ ] Race detail pages with qualifying results
- [ ] Multi-season support
- [ ] AWS deployment (EC2 + RDS)


## Author

Hansol Ji - [GitHub](https://github.com/jihansol1)
