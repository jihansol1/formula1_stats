package com.sol.f1stats.model;

import jakarta.persistence.*;
import java.time.LocalDate;

@Entity
@Table(name = "races")
public class Race {

    @Id
    @Column(name = "race_id")
    private Integer raceId;

    @Column(name = "name")
    private String name;

    @Column(name = "circuit")
    private String circuit;

    @Column(name = "country")
    private String country;

    @Column(name = "date")
    private LocalDate date;

    @Column(name = "season")
    private Integer season;

    // Default constructor
    public Race() {}

    // Getters and Setters
    public Integer getRaceId() { return raceId; }
    public void setRaceId(Integer raceId) { this.raceId = raceId; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getCircuit() { return circuit; }
    public void setCircuit(String circuit) { this.circuit = circuit; }

    public String getCountry() { return country; }
    public void setCountry(String country) { this.country = country; }

    public LocalDate getDate() { return date; }
    public void setDate(LocalDate date) { this.date = date; }

    public Integer getSeason() { return season; }
    public void setSeason(Integer season) { this.season = season; }
}