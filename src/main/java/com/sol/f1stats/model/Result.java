package com.sol.f1stats.model;

import jakarta.persistence.*;

@Entity
@Table(name = "results")
public class Result {

    @Id
    @Column(name = "result_id")
    private Integer resultId;

    @Column(name = "race_id")
    private Integer raceId;

    @Column(name = "driver_id")
    private String driverId;

    @Column(name = "position")
    private Integer position;

    @Column(name = "points")
    private Integer points;

    @Column(name = "grid_position")
    private Integer gridPosition;

    @Column(name = "status")
    private String status;

    @Column(name = "fastest_lap")
    private String fastestLap;

    @Column(name = "is_sprint")
    private Boolean isSprint;

    @Column(name = "constructor_id")
    private String constructorId;

    // Default constructor
    public Result() {}

    // Getters and Setters
    public Integer getResultId() { return resultId; }
    public void setResultId(Integer resultId) { this.resultId = resultId; }

    public Integer getRaceId() { return raceId; }
    public void setRaceId(Integer raceId) { this.raceId = raceId; }

    public String getDriverId() { return driverId; }
    public void setDriverId(String driverId) { this.driverId = driverId; }

    public Integer getPosition() { return position; }
    public void setPosition(Integer position) { this.position = position; }

    public Integer getPoints() { return points; }
    public void setPoints(Integer points) { this.points = points; }

    public Integer getGridPosition() { return gridPosition; }
    public void setGridPosition(Integer gridPosition) { this.gridPosition = gridPosition; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public String getFastestLap() { return fastestLap; }
    public void setFastestLap(String fastestLap) { this.fastestLap = fastestLap; }

    public Boolean getIsSprint() { return isSprint; }
    public void setIsSprint(Boolean isSprint) { this.isSprint = isSprint; }

    public String getConstructorId() { return constructorId; }

    public void setConstructorId(String constructorId) { this.constructorId = constructorId; }
}