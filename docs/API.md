# API reference

Base URL: `http://localhost:8080`

| Method | Path | Purpose | Success |
|---|---|---|---|
| POST | `/api/v1/tasks` | Create a task | 201 |
| GET | `/api/v1/tasks` | List paged tasks | 200 |
| GET | `/api/v1/tasks/search?status={status}` | List paged tasks with a status | 200 |
| GET | `/api/v1/tasks/{id}` | Read one task | 200 |
| PATCH | `/api/v1/tasks/{id}` | Partially update a task | 200 |
| DELETE | `/api/v1/tasks/{id}` | Delete a task | 204 |
| GET | `/actuator/health` | Health check | 200 |

## Create body

```json
{"title":"Learn Claude hooks","description":"Build the sample","dueDate":"2026-12-01"}
```

`title` is required and limited to 120 characters. `description` is optional and limited to 1000.

## Update body

All properties are optional. Omit an unchanged property.

```json
{"title":"Use Claude hooks","status":"IN_PROGRESS","dueDate":"2026-12-05"}
```

## Pagination

`GET /api/v1/tasks?page=0&size=10&sort=dueDate,asc`

## Search by status

`GET /api/v1/tasks/search?status=IN_PROGRESS&page=0&size=10`

`status` is required and must be `TODO`, `IN_PROGRESS`, or `DONE`; otherwise the API returns 400.
The response is paged like the list endpoint and accepts the same `page`, `size`, and `sort`.

## Error shape

```json
{
  "timestamp":"2026-11-21T10:00:00Z",
  "status":400,
  "error":"Validation failed",
  "details":{"title":"must not be blank"}
}
```
