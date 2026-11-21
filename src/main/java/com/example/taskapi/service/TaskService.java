package com.example.taskapi.service;
import com.example.taskapi.domain.TaskItem;
import com.example.taskapi.domain.TaskStatus;
import com.example.taskapi.dto.*;
import com.example.taskapi.exception.TaskNotFoundException;
import com.example.taskapi.repository.TaskRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
@Service
@Transactional
@RequiredArgsConstructor
public class TaskService {
    private final TaskRepository repository;

    @Transactional(readOnly = true)
    public Page<TaskResponse> list(Pageable pageable) {
        return repository.findAll(pageable).map(TaskResponse::from);
    }

    @Transactional(readOnly = true)
    public Page<TaskResponse> searchByStatus(TaskStatus status, Pageable pageable) {
        return repository.findByStatus(status, pageable).map(TaskResponse::from);
    }

    @Transactional(readOnly = true)
    public TaskResponse get(Long id) {
        return TaskResponse.from(find(id));
    }

    public TaskResponse create(CreateTaskRequest request) {
        TaskItem task = new TaskItem();
        task.setTitle(request.title().trim());
        task.setDescription(request.description());
        task.setDueDate(request.dueDate());
        return TaskResponse.from(repository.save(task));
    }

    public TaskResponse update(Long id, UpdateTaskRequest request) {
        TaskItem task = find(id);
        if (request.title() != null) task.setTitle(request.title().trim());
        if (request.description() != null) task.setDescription(request.description());
        if (request.status() != null) task.setStatus(request.status());
        if (request.dueDate() != null) task.setDueDate(request.dueDate());
        return TaskResponse.from(repository.save(task));
    }

    public void delete(Long id) {
        repository.delete(find(id));
    }

    private TaskItem find(Long id) {
        return repository.findById(id).orElseThrow(() -> new TaskNotFoundException(id));
    }
}
