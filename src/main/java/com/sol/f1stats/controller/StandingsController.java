package com.sol.f1stats.controller;

import com.sol.f1stats.dto.ConstructorStandingDTO;
import com.sol.f1stats.dto.DriverStandingDTO;
import com.sol.f1stats.service.StandingsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/standings")
@CrossOrigin(origins = "*")
public class StandingsController {
    @Autowired
    private StandingsService standingsService;

    @GetMapping("/drivers")
    public List<DriverStandingDTO> getDriverStandings(@RequestParam Integer upToRaceId) {
        return standingsService.getDriverStandingsUpToRace(upToRaceId);
    }
    @GetMapping("/constructors")
    public List<ConstructorStandingDTO> getConstructorStandings(@RequestParam Integer upToRaceId) {
        return standingsService.getConstructorStandingsUpToRace(upToRaceId);
    }
}
