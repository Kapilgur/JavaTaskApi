package com.example.taskapi;

import com.example.taskapi.domain.TaskItem;
import com.example.taskapi.repository.TaskRepository;
import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
class TaskLifecycleTest {
    @Autowired MockMvc mvc;
    @Autowired TaskRepository repository;

    @BeforeEach void clean() { repository.deleteAll(); }

    @Test
    void updatesAndDeletesTask() throws Exception {
        TaskItem task = new TaskItem();
        task.setTitle("Initial");
        Long id = repository.save(task).getId();
        mvc.perform(patch("/api/v1/tasks/{id}", id).contentType(MediaType.APPLICATION_JSON)
                        .content("{\"title\":\"Updated\",\"status\":\"DONE\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.title").value("Updated"))
                .andExpect(jsonPath("$.status").value("DONE"));
        mvc.perform(delete("/api/v1/tasks/{id}", id))
                .andExpect(status().isNoContent());
        mvc.perform(get("/api/v1/tasks/{id}", id))
                .andExpect(status().isNotFound());
    }

    @Test
    void returnsNotFound() throws Exception {
        mvc.perform(get("/api/v1/tasks/999999"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.error").value("Task 999999 was not found"));
    }
}
