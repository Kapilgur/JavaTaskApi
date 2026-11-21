---
name: java-rest-api
description: Safely extend this Spring Boot task API while preserving its layering, tests, and small, focused source files.
---

# Java REST API skill

1. Follow the `safe-git-workflow` skill: work on a task branch, never on a protected branch.
2. Read `CLAUDE.md` and only the files for the layer being changed.
3. Keep classes small; add at most 50 new lines per `Write`/`Edit` (hook-enforced).
4. Preserve Controller -> Service -> Repository -> MySQL separation.
5. Add or update a focused integration test for behavior changes.
6. Run `./mvnw test` (`mvnw.cmd test` on Windows).
7. Report changed files, tests, and any unresolved risk; do not commit or push unless approved.
