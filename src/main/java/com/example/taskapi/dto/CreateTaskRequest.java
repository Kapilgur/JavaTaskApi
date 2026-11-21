package com.example.taskapi.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import java.time.LocalDate;

public record CreateTaskRequest(
        @NotBlank @Size(max = 120) String title,
        @Size(max = 1000) String description,
        LocalDate dueDate) {}
