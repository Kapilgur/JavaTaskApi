package com.example.taskapi;

import com.example.taskapi.domain.TaskItem;
import com.example.taskapi.domain.TaskStatus;
import com.example.taskapi.repository.TaskRepository;
import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
class TaskSearchTest {
    @Autowired MockMvc mvc;
    @Autowired TaskRepository repository;

    @BeforeEach
    void seed() {
        repository.deleteAll();
        save("Write code", TaskStatus.IN_PROGRESS);
        save("Plan work", TaskStatus.TODO);
        save("Ship it", TaskStatus.IN_PROGRESS);
    }

    @Test
    void returnsOnlyTasksWithRequestedStatus() throws Exception {
        mvc.perform(get("/api/v1/tasks/search").param("status", "IN_PROGRESS"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.totalElements").value(2))
                .andExpect(jsonPath("$.content[0].title").value("Write code"))
                .andExpect(jsonPath("$.content[1].title").value("Ship it"));
    }

    @Test
    void returnsEmptyPageWhenNoMatch() throws Exception {
        mvc.perform(get("/api/v1/tasks/search").param("status", "DONE"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.totalElements").value(0));
    }

    @Test
    void rejectsUnknownStatus() throws Exception {
        mvc.perform(get("/api/v1/tasks/search").param("status", "BOGUS"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.details.status").exists());
    }

    @Test
    void rejectsMissingStatus() throws Exception {
        mvc.perform(get("/api/v1/tasks/search"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.details.status").value("is required"));
    }

    private void save(String title, TaskStatus status) {
        TaskItem task = new TaskItem();
        task.setTitle(title);
        task.setStatus(status);
        repository.save(task);
    }
}
