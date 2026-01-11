package com.sol.f1stats.controller;

import com.sol.f1stats.model.Race;
import com.sol.f1stats.repository.RaceRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/races")
@CrossOrigin(origins = "*")
public class RaceController {
    @Autowired
    private RaceRepository raceRepository;

    // GET /api/races - Get all races for the timeline
    @GetMapping
    public List<Race> getAllRaces() {
        return raceRepository.findAllByOrderByDateAsc();
    }

    // Get specific race details
    @GetMapping("/{raceId}")
    public Race getRace(@PathVariable Integer raceId) {
        return raceRepository.findById(raceId)
                .orElseThrow(() -> new RuntimeException("Race with id " + raceId + " not found"));
    }

    // Get all races for a season
    @GetMapping("/season/{season}")
    public List<Race> getRacesBySeason(@PathVariable Integer season) {
        return raceRepository.findBySeasonOrderByDateAsc(season);
    }
}
