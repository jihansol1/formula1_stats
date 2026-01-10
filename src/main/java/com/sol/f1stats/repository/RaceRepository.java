package com.sol.f1stats.repository;

import com.sol.f1stats.model.Race;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface RaceRepository extends JpaRepository<Race, Integer> {
    List<Race> findBySeasonOrderByDateAsc(Integer season);
    List<Race> findAllByOrderByDateAsc();
}