package com.example.taskapi.dto;

import com.example.taskapi.domain.TaskItem;
import com.example.taskapi.domain.TaskStatus;
import java.time.Instant;
import java.time.LocalDate;

public record TaskResponse(
        Long id,
        String title,
        String description,
        TaskStatus status,
        LocalDate dueDate,
        Instant createdAt,
        Instant updatedAt) {
    public static TaskResponse from(TaskItem task) {
        return new TaskResponse(task.getId(), task.getTitle(), task.getDescription(),
                task.getStatus(), task.getDueDate(), task.getCreatedAt(), task.getUpdatedAt());
    }
}
