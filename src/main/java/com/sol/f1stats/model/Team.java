package com.sol.f1stats.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "teams")
public class Team {
    @Id
    @Column(name = "team_id")
    private String teamId;

    @Column(name = "name")
    private String name;

    @Column(name = "nationality")
    private String nationality;

    @Column(name = "points")
    private Integer points;

    @Column(name = "wins")
    private Integer wins;

    @Column(name = "podiums")
    private Integer podiums;

    // Default Constructor
    public Team() {}

    // Getters and Setters
    public String getTeamId() { return teamId; }
    public void setTeamId(String teamId) { this.teamId = teamId; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getNationality() { return nationality; }
    public void setNationality(String nationality) { this.nationality = nationality; }

    public Integer getPoints() { return points; }
    public void setPoints(Integer points) { this.points = points; }

    public Integer getWins() { return wins; }
    public void setWins(Integer wins) { this.wins = wins; }

    public Integer getPodiums() { return podiums; }
    public void setPodiums(Integer podiums) { this.podiums = podiums; }




}
