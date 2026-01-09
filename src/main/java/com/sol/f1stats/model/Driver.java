package com.sol.f1stats.model;

import jakarta.persistence.*;

@Entity
@Table(name = "drivers")
public class Driver {

    @Id
    @Column(name = "driver_id")
    private String driverId;

    @Column(name = "name")
    private String name;

    @Column(name = "team_id")
    private String teamId;

    @Column(name = "nationality")
    private String nationality;

    @Column(name = "number")
    private Integer number;

    @Column(name = "points")
    private Integer points;

    @Column(name = "wins")
    private Integer wins;

    @Column(name = "podiums")
    private Integer podiums;

    @Column(name = "poles")
    private Integer poles;

    // Default constructor
    public Driver() {}

    // Getters and Setters
    public String getDriverId() { return driverId; }
    public void setDriverId(String driverId) { this.driverId = driverId; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getTeamId() { return teamId; }
    public void setTeamId(String teamId) { this.teamId = teamId; }

    public String getNationality() { return nationality; }
    public void setNationality(String nationality) { this.nationality = nationality; }

    public Integer getNumber() { return number; }
    public void setNumber(Integer number) { this.number = number; }

    public Integer getPoints() { return points; }
    public void setPoints(Integer points) { this.points = points; }

    public Integer getWins() { return wins; }
    public void setWins(Integer wins) { this.wins = wins; }

    public Integer getPodiums() { return podiums; }
    public void setPodiums(Integer podiums) { this.podiums = podiums; }

    public Integer getPoles() { return poles; }
    public void setPoles(Integer poles) { this.poles = poles; }
}