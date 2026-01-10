package com.sol.f1stats.repository;

import com.sol.f1stats.model.Driver;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface DriverRepository extends JpaRepository<Driver, String> {
    List<Driver> findAllByOrderByPointsDesc();
    List<Driver> findByTeamId(String teamId);
}