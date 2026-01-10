package com.sol.f1stats.repository;

import com.sol.f1stats.model.Result;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.util.List;

public interface ResultRepository extends JpaRepository<Result, Integer> {

    List<Result> findByRaceId(Integer raceId);

    List<Result> findByDriverId(String driverId);

    @Query("SELECT r FROM Result r WHERE r.raceId IN :raceIds")
    List<Result> findByRaceIdIn(@Param("raceIds") List<Integer> raceIds);
}