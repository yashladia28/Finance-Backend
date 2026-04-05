# Finance Dashboard API

A backend REST API for a finance dashboard system with role-based access control, built with FastAPI and MongoDB.

---

## Tech Stack

- Python 3.14
- FastAPI
- MongoDB Atlas
- pymongo

---

## Project Structure

    finance-backend/
    ├── main.py        — all API routes
    ├── models.py      — Pydantic data models
    ├── database.py    — MongoDB connection
    ├── auth.py        — role checking dependency
    ├── .env.example   — environment variable template
    └── README.md      — this file

---

## Setup

1. Clone the repository

2. Install dependencies:

        pip install fastapi uvicorn pymongo python-dotenv pydantic

3. Copy `.env.example` to `.env` and fill in your MongoDB credentials:

        MONGODB_URI=your_mongodb_connection_string
        DB_NAME=financeapp

4. Run the server:

        uvicorn main:app --reload

5. Visit `http://localhost:8000/docs` for interactive API documentation

---

## Authentication

This API uses simplified header-based authentication. Pass the MongoDB ID of an existing user as a request header with every request:

    x-user-id: <user_id>

---

## Roles

| Role    | Permissions                                      |
|---------|--------------------------------------------------|
| admin   | Full access — manage users and records           |
| analyst | View and create/update records, view dashboard   |
| viewer  | Read-only access to records and dashboard        |

---

## API Endpoints

### Users

| Method | Route          | Access    | Description       |
|--------|----------------|-----------|-------------------|
| POST   | /users         | admin     | Create a new user |
| GET    | /users         | all roles | Get all users     |
| GET    | /users/{id}    | all roles | Get user by ID    |
| PATCH  | /users/{id}    | admin     | Update user       |
| DELETE | /users/{id}    | admin     | Delete user       |

### Records

| Method | Route           | Access        | Description                                                                 |
|--------|-----------------|---------------|-----------------------------------------------------------------------------|
| POST   | /records        | admin/analyst | Create a financial record                                                   |
| GET    | /records        | all roles     | Get records with optional filters (?type, ?category, ?date) and pagination (?page, ?limit) |
| GET    | /records/{id}   | all roles     | Get record by ID                                                            |
| PATCH  | /records/{id}   | admin/analyst | Update a record                                                             |
| DELETE | /records/{id}   | admin         | Delete a record                                                             |

### Dashboard

| Method | Route                | Access    | Description                        |
|--------|----------------------|-----------|------------------------------------|
| GET    | /dashboard/summary  | all roles | Total income, expenses, net balance |
| GET    | /dashboard/category | all roles | Totals grouped by category         |
| GET    | /dashboard/recent   | all roles | Last 5 transactions                |

---

## Design Decisions

- Role checks are applied on all routes including GET routes to allow easy extension if new restricted roles are added in the future
- Separate Create, Update, and Out models are used for each entity to avoid exposing sensitive fields like passwords in API responses
- Pagination is implemented on GET /records using skip/limit — defaults to page 1 with 10 records per page
- Authentication uses header-based user identification instead of JWT tokens to keep the implementation focused on backend structure and access control logic

---

## Assumptions

- User identity is passed via the `x-user-id` header instead of JWT tokens
- Passwords are stored as plain text — in production these would be hashed using bcrypt or similar
- The `created_by` field in records is provided by the caller — in production this would be extracted from the auth token automatically
- MongoDB connection string is hardcoded for development — in production this should be moved to environment variables
