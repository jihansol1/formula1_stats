package com.sol.f1stats.dto;

public class DriverStandingDTO {
    private int position;
    private String driverId;
    private String name;
    private String teamId;
    private int points;
    private int wins;
    private int podiums;

    // Constructor
    private DriverStandingDTO(String driverId, String name, String teamId, int position, int points,
                                     int wins, int podiums) {
        this.driverId = driverId;
        this.teamId = teamId;
        this.position = position;
        this.points = (int) points;
        this.wins = (int) wins;
        this.podiums = (int) podiums;
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
