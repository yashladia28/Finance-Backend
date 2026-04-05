# Finance Dashboard API

A backend REST API for a finance dashboard system with role-based access control, built with FastAPI and MongoDB.

## Tech Stack
- Python 3.14
- FastAPI
- MongoDB Atlas
- pymongo

## Setup

1. Clone the repository
2. Install dependencies:
   pip install fastapi uvicorn pymongo python-dotenv pydantic
3. Create a `.env` file:
   MONGODB_URI=your_mongodb_connection_string
   DB_NAME=financeapp
4. Run the server:
   uvicorn main:app --reload
5. Visit http://localhost:8000/docs for interactive API documentation

## Roles
| Role | Permissions |
|---|---|
| admin | Full access — manage users and records |
| analyst | View and create/update records, view dashboard |
| viewer | Read-only access to records and dashboard |

## Authentication
Pass the user's MongoDB ID as a request header:
x-user-id: <user_id>

## Design Decisions
- Role checks are applied even on GET routes to allow easy extension 
  if new restricted roles are added in the future
- Separate Create/Update/Out models are used for each entity to avoid 
  exposing sensitive fields like passwords in responses

## API Endpoints

### Users
| Method | Route | Access | Description |
|---|---|---|---|
| POST | /users | admin | Create a new user |
| GET | /users | all roles | Get all users |
| GET | /users/{id} | all roles | Get user by ID |
| PATCH | /users/{id} | admin | Update user |
| DELETE | /users/{id} | admin | Delete user |

### Records
| Method | Route | Access | Description |
|---|---|---|---|
| POST | /records | admin, analyst | Create a financial record |
| GET | /records | all roles | Get all records (supports ?type, ?category, ?date filters) |
| GET | /records/{id} | all roles | Get record by ID |
| PATCH | /records/{id} | admin, analyst | Update a record |
| DELETE | /records/{id} | admin | Delete a record |

### Dashboard
| Method | Route | Access | Description |
|---|---|---|---|
| GET | /dashboard/summary | all roles | Total income, expenses, net balance |
| GET | /dashboard/category | all roles | Totals grouped by category |
| GET | /dashboard/recent | all roles | Last 5 transactions |

## Assumptions
- Authentication is simplified — user identity is passed via the x-user-id header instead of JWT tokens
- Passwords are stored as plain text — in production these would be hashed
- The created_by field in records is provided by the caller for now

## Project Structure
finance-backend/
├── main.py        — all API routes
├── models.py      — Pydantic data models
├── database.py    — MongoDB connection
├── auth.py        — role checking dependency
└── README.md      — this file

## Note on Configuration
Connection string is hardcoded for development. 
In production, move to environment variables.

## Setup
1. Copy `.env.example` to `.env`
2. Fill in your MongoDB credentials
3. Run `uvicorn main:app --reload`