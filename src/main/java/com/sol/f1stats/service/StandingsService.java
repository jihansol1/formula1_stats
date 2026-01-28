package com.sol.f1stats.service;

import com.sol.f1stats.dto.ConstructorStandingDTO;
import com.sol.f1stats.dto.DriverStandingDTO;
import com.sol.f1stats.model.Driver;
import com.sol.f1stats.model.Race;
import com.sol.f1stats.model.Result;
import com.sol.f1stats.model.Team;
import com.sol.f1stats.repository.DriverRepository;
import com.sol.f1stats.repository.RaceRepository;
import com.sol.f1stats.repository.ResultRepository;
import com.sol.f1stats.repository.TeamRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class StandingsService {

    @Autowired
    private RaceRepository raceRepository;

    @Autowired
    private ResultRepository resultRepository;

    @Autowired
    private DriverRepository driverRepository;

    @Autowired
    private TeamRepository teamRepository;

    // Get Driver Standings up to and including a specific race (within same season)
    public List<DriverStandingDTO> getDriverStandingsUpToRace(int raceId) {
        // Get the target race to find its date and season
        Race targetRace = raceRepository.findById(raceId)
                .orElseThrow(() -> new RuntimeException("Race not found: " + raceId));

        Integer targetSeason = targetRace.getSeason();

        // Get all races in the SAME SEASON up to and including this date
        List<Race> racesUpTo = raceRepository.findBySeasonOrderByDateAsc(targetSeason).stream()
                .filter(r -> !r.getDate().isAfter(targetRace.getDate()))
                .collect(Collectors.toList());

        // Extract race IDs
        List<Integer> raceIds = racesUpTo.stream()
                .map(Race::getRaceId)
                .collect(Collectors.toList());

        // Get all results for these races
        List<Result> results = resultRepository.findByRaceIdIn(raceIds);

        // Get all drivers for name lookup
        Map<String, Driver> driverMap = driverRepository.findAll().stream()
                .collect(Collectors.toMap(Driver::getDriverId, d -> d));

        // Aggregate stats per driver: [points, wins, podiums]
        Map<String, int[]> driverStats = new HashMap<>();

        for (Result result : results) {
            String driverId = result.getDriverId();
            driverStats.putIfAbsent(driverId, new int[]{0, 0, 0});

            int[] stats = driverStats.get(driverId);
            stats[0] += result.getPoints() != null ? result.getPoints() : 0;

            // Only count wins/podiums for main races, not sprints
            Boolean isSprint = result.getIsSprint();
            if (isSprint == null || !isSprint) {
                if (result.getPosition() != null && result.getPosition() == 1) stats[1]++;
                if (result.getPosition() != null && result.getPosition() <= 3) stats[2]++;
            }
        }

        // Convert to DTOs
        List<DriverStandingDTO> standings = new ArrayList<>();
        for (Map.Entry<String, int[]> entry : driverStats.entrySet()) {
            String driverId = entry.getKey();
            int[] stats = entry.getValue();
            Driver driver = driverMap.get(driverId);

            if (driver != null) {
                standings.add(new DriverStandingDTO(
                        driverId,
                        driver.getName(),
                        driver.getTeamId(),
                        stats[0], stats[1], stats[2]
                ));
            }
        }

        // Sort by points descending
        standings.sort((a, b) -> Integer.compare(b.getPoints(), a.getPoints()));

        // Set Positions
        for (int i = 0; i < standings.size(); i++) {
            standings.get(i).setPosition(i + 1);
        }
        return standings;
    }

    // Get Constructor Standings up to and including a specific race (within same season)
    public List<ConstructorStandingDTO> getConstructorStandingsUpToRace(Integer raceId) {
        // Get the target race to find its date and season
        Race targetRace = raceRepository.findById(raceId)
                .orElseThrow(() -> new RuntimeException("Race not found: " + raceId));

        Integer targetSeason = targetRace.getSeason();

        // Get all races in the SAME SEASON up to and including this date
        List<Race> racesUpTo = raceRepository.findBySeasonOrderByDateAsc(targetSeason).stream()
                .filter(r -> !r.getDate().isAfter(targetRace.getDate()))
                .collect(Collectors.toList());

        // Extract race IDs
        List<Integer> raceIds = racesUpTo.stream()
                .map(Race::getRaceId)
                .collect(Collectors.toList());

        // Get all results for these races
        List<Result> results = resultRepository.findByRaceIdIn(raceIds);

        // Get all teams for name lookup
        Map<String, Team> teamMap = teamRepository.findAll().stream()
                .collect(Collectors.toMap(Team::getTeamId, t -> t));

        // Aggregate stats per constructor: [points, wins, podiums]
        // Use constructor_id from results (team at time of race)
        Map<String, int[]> constructorStats = new HashMap<>();

        for (Result result : results) {
            String teamId = result.getConstructorId();
            if (teamId == null) continue;

            constructorStats.putIfAbsent(teamId, new int[]{0, 0, 0});

            int[] stats = constructorStats.get(teamId);
            stats[0] += result.getPoints() != null ? result.getPoints() : 0;

            // Only count wins/podiums for main races, not sprints
            Boolean isSprint = result.getIsSprint();
            if (isSprint == null || !isSprint) {
                if (result.getPosition() != null && result.getPosition() == 1) stats[1]++;
                if (result.getPosition() != null && result.getPosition() <= 3) stats[2]++;
            }
        }

        // Convert to DTOs
        List<ConstructorStandingDTO> standings = new ArrayList<>();
        for (Map.Entry<String, int[]> entry : constructorStats.entrySet()) {
            String teamId = entry.getKey();
            int[] stats = entry.getValue();
            Team team = teamMap.get(teamId);

            if (team != null) {
                standings.add(new ConstructorStandingDTO(
                        teamId,
                        team.getName(),
                        stats[0], stats[1], stats[2]
                ));
            }
        }

        // Sort by points descending
        standings.sort((a, b) -> Integer.compare(b.getPoints(), a.getPoints()));

        // Set positions
        for (int i = 0; i < standings.size(); i++) {
            standings.get(i).setPosition(i + 1);
        }

        return standings;
    }
}