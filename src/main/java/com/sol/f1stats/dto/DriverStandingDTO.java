package com.sol.f1stats.dto;

public class DriverStandingDTO {
    private int position;
    private String driverId;
    private String name;
    private String teamId;
    private int points;
    private int wins;
    private int podiums;

    // Constructor - 6 parameters (without position, it gets set later)
    public DriverStandingDTO(String driverId, String name, String teamId, int points, int wins, int podiums) {
        this.driverId = driverId;
        this.name = name;
        this.teamId = teamId;
        this.points = points;
        this.wins = wins;
        this.podiums = podiums;
    }

    // Getters and Setters
    public int getPosition() { return position; }
    public void setPosition(int position) { this.position = position; }

    public String getDriverId() { return driverId; }
    public String getName() { return name; }
    public String getTeamId() { return teamId; }
    public int getPoints() { return points; }
    public int getWins() { return wins; }
    public int getPodiums() { return podiums; }
}