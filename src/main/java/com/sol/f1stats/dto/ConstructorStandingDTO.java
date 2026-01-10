package com.sol.f1stats.dto;

public class ConstructorStandingDTO {
    private int position;
    private String teamId;
    private String name;
    private int points;
    private int wins;
    private int podiums;

    // Constructor
    public ConstructorStandingDTO(int position, String teamId, String name, int points, int wins, int podiums) {
        this.position = position;
        this.teamId = teamId;
        this.name = name;
        this.points = points;
        this.wins = wins;
        this.podiums = podiums;
    }

    // Getters and Setters
    public int getPosition() { return position; }
    public void setPosition(int position) { this.position = position; }

    public String getTeamId() { return teamId; }
    public String getName() { return name; }
    public int getPoints() { return points; }
    public int getWins() { return wins; }
    public int getPodiums() { return podiums; }

}
