package com.example.taskapi.dto;

import com.example.taskapi.domain.TaskStatus;
import jakarta.validation.constraints.Size;
import java.time.LocalDate;

public record UpdateTaskRequest(
        @Size(min = 1, max = 120) String title,
        @Size(max = 1000) String description,
        TaskStatus status,
        LocalDate dueDate) {}
