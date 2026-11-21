package com.example.taskapi;

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
class TaskControllerTest {
    @Autowired MockMvc mvc;
    @Autowired TaskRepository repository;

    @BeforeEach void clean() { repository.deleteAll(); }

    @Test
    void createsAndReadsTask() throws Exception {
        String json = """
                {"title":"Learn hooks","description":"Limit source files","dueDate":"2026-12-01"}
                """;
        mvc.perform(post("/api/v1/tasks").contentType(MediaType.APPLICATION_JSON).content(json))
                .andExpect(status().isCreated())
                .andExpect(header().string("Location", org.hamcrest.Matchers.containsString("/api/v1/tasks/")))
                .andExpect(jsonPath("$.title").value("Learn hooks"))
                .andExpect(jsonPath("$.status").value("TODO"));
        mvc.perform(get("/api/v1/tasks"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content[0].description").value("Limit source files"));
    }

    @Test
    void rejectsBlankTitle() throws Exception {
        mvc.perform(post("/api/v1/tasks").contentType(MediaType.APPLICATION_JSON)
                        .content("{\"title\":\" \"}"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.details.title").exists());
    }
}
