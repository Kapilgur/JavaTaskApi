package com.example.taskapi.repository;

import com.example.taskapi.domain.TaskItem;
import com.example.taskapi.domain.TaskStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TaskRepository extends JpaRepository<TaskItem, Long> {
    Page<TaskItem> findByStatus(TaskStatus status, Pageable pageable);
}
