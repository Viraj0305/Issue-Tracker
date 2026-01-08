Issue Tracker Backend (FastAPI + PostgreSQL)

Overview
A production-style backend service built using FastAPI and PostgreSQL that allows users to manage issues, comments, and labels.
The project demonstrates real-world backend concepts such as optimistic concurrency control, transactions, CSV imports, and robust error handling.

Features
- Issue management (CRUD operations)
- Optimistic concurrency control using versioning
- Comment system with author validation
- Unique labels with atomic assignment
- Transactional bulk status updates
- CSV import for bulk issue creation
- Aggregated reports
- Bonus: Issue timeline showing issue history

Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Swagger (OpenAPI)

Project Structure
app/
- main.py
- database.py
- models.py
- schemas.py
- deps.py
- utils.py
routers/
- issues.py
- reports.py
- timeline.py

Setup Instructions
1. Clone the repository
2. Create and activate virtual environment
3. Install dependencies using requirements.txt
4. Configure PostgreSQL database
5. Run the application using uvicorn

API Endpoints
Issues:
- POST /issues
- GET /issues
- GET /issues/{id}
- PATCH /issues/{id}
- POST /issues/{id}/comments
- PUT /issues/{id}/labels
- POST /issues/bulk-status
- POST /issues/import
- GET /issues/{id}/timeline

Reports:
- GET /reports/top-assignees
- GET /reports/latency

CSV Import
- Supports bulk issue creation
- Skips invalid rows
- Returns row-level error report

Error Handling
- Request validation errors (422)
- Resource not found errors (404)
- Version conflict errors (409)
- Database constraint handling
- Transaction rollback for bulk operations

Design Notes
- Optimistic locking prevents lost updates
- Database constraints ensure integrity
- Timeline provides audit trail



