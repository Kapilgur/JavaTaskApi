package com.example.taskapi.repository;

import com.example.taskapi.domain.TaskItem;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TaskRepository extends JpaRepository<TaskItem, Long> {}
