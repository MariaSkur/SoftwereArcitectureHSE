package com.example.controller;

import com.example.model.Project;
import com.example.repository.ProjectRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/projects")
@CrossOrigin(origins = "*") // разрешаем запросы с любого источника (для простоты)
public class ProjectController {

    @Autowired
    private ProjectRepository projectRepository;

    // GET /api/projects – получить все проекты
    @GetMapping
    public List<Project> getAllProjects() {
        return projectRepository.findAll();
    }

    // POST /api/projects – создать новый проект
    @PostMapping
    public Project createProject(@RequestBody Project project) {
        return projectRepository.save(project);
    }
}
