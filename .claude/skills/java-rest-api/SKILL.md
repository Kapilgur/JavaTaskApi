---
name: java-rest-api
description: Safely extend this Spring Boot task API while preserving its layering, tests, and 50-line source-file limit.
---

# Java REST API skill

1. Read `CLAUDE.md` and only the files for the layer being changed.
2. Keep every source file at 50 physical lines or fewer.
3. Preserve Controller -> Service -> Repository -> MySQL separation.
4. Add or update a focused integration test for behavior changes.
5. Run `./mvnw test` (`mvnw.cmd test` on Windows).
6. Report changed files, tests, and any unresolved risk; do not commit or push unless asked.
