package com.example.app;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@SpringBootApplication
@RestController
@RequestMapping("/api")
public class Application {

    private List<String> venues = new ArrayList<>();

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    // тест 1
    @GetMapping("/health")
    public String health() {
        return "OK";
    }

    // тест 2
    @GetMapping("/venues")
    public List<String> getVenues() {
        return venues;
    }

    // тест 3
    @PostMapping("/venues")
    public String addVenue(@RequestBody String venue) {
        venues.add(venue);
        return "Venue added";
    }

    // тест 4
    @GetMapping("/venues/count")
    public int countVenues() {
        return venues.size();
    }

    // тест 5
    @DeleteMapping("/venues")
    public String clearVenues() {
        venues.clear();
        return "All venues deleted";
    }
}
