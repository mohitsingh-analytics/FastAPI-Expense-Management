# FastAPI Expense Management API

A hands-on **FastAPI REST API** built as part of an AI Architect / Forward Deployed Engineering learning journey.

The project starts with a simple CSV-backed expense service and focuses on understanding the fundamentals of modern API development: REST endpoints, request validation, Pydantic models, CRUD operations, persistence, error handling, and automated API testing.

> **Learning philosophy:** Build a small working system first, understand every layer, and progressively evolve it toward production-grade architecture.

---

## 🎯 Project Goals

This project is intentionally small, but it is designed to demonstrate the engineering concepts that sit underneath larger enterprise services.

The primary goals are to understand:

- How FastAPI exposes Python functions as HTTP APIs
- REST resource and endpoint design
- Path parameters and automatic request validation
- Pydantic models as API contracts
- Creating and validating request bodies
- CRUD API implementation
- HTTP status codes and error handling
- Basic persistence using Pandas and CSV
- Automated API testing with Pytest
- The difference between API behavior and implementation details
- How a simple API can be progressively evolved toward production architecture

---

## 🏗️ Current Architecture

The current version deliberately uses CSV as the persistence layer so that the API concepts remain easy to understand.

```text
                    HTTP Client
                        │
                        ▼
                ┌───────────────┐
                │    FastAPI    │
                │   API Layer   │
                └───────┬───────┘
                        │
             Request validation
                        │
                        ▼
                ┌───────────────┐
                │    Pydantic   │
                │  Data Models  │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │ Python /       │
                │ Pandas Logic  │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │ CSV Persistence│
                └───────────────┘
```

### Important architectural note

The CSV implementation is intentionally educational.

For a production workload with hundreds of millions of records, loading and rewriting an entire CSV file would not be an appropriate persistence strategy. A production design would typically introduce a database, transactional data store, or a lakehouse technology such as Delta Lake depending on the workload and access pattern.

This project is therefore a **foundation**, not a claim that CSV is a production-scale data architecture.

---

## ✨ Features

### API

- Health check endpoint
- Retrieve all expenses
- Retrieve an expense by ID
- Create a new expense
- Partially update an existing expense
- Delete an expense
- Automatic path parameter validation
- HTTP 404 handling for missing resources
- Pydantic request validation

### Data

- CSV-based persistence
- Automatic next-ID generation using the maximum existing ID + 1
- Create/update/delete operations persisted back to the CSV file

### Testing

- Pytest-based API testing
- FastAPI `TestClient`
- Health endpoint test
- Expense creation test
- Invalid request validation test

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application language |
| FastAPI | REST API framework |
| Pydantic | Request models and validation |
| Pandas | Data manipulation and CSV persistence |
| Uvicorn | ASGI application server |
| Pytest | Automated testing |
| HTTPX | HTTP client support for API testing |
| Swagger / OpenAPI | Interactive API documentation |

---

## 📁 Project Structure

```text
fastapi-expense-management-api/
│
├── main.py
├── sample_expenses.csv
├── requirements.txt
├── README.md
│
└── tests/
    └── test_api.py
```

The project intentionally starts with a simple structure. A later iteration will separate the API, business logic, and persistence/data-access layers.

---

# 🚀 Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/mohitsingh-analytics/fastapi-expense-management-api.git
cd fastapi-expense-management-api
```

## 2. Create a virtual environment

### Windows

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

If dependencies have not yet been captured in `requirements.txt`, install the core packages:

```bash
pip install fastapi uvicorn pandas pydantic pytest httpx
```

## 4. Start the API

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

# 📚 API Documentation

FastAPI automatically generates interactive API documentation.

### Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

### ReDoc

Open:

```text
http://127.0.0.1:8000/redoc
```

Swagger is particularly useful during development because requests can be executed directly from the browser.

---

# 🔌 API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Basic application response |
| GET | `/health` | Health check |
| GET | `/expenses` | Retrieve all expenses |
| GET | `/expenses/{expense_id}` | Retrieve one expense |
| POST | `/expenses` | Create an expense |
| PATCH | `/expenses/{expense_id}` | Partially update an expense |
| DELETE | `/expenses/{expense_id}` | Delete an expense |

---

## GET `/expenses`

Returns the collection of expenses.

Example:

```http
GET /expenses
```

The API reads the CSV and returns the records as JSON.

---

## GET `/expenses/{expense_id}`

Returns a specific expense.

Example:

```http
GET /expenses/5
```

If the ID does not exist:

```json
{
  "detail": "Expense not found"
}
```

The API returns HTTP `404`.

---

## POST `/expenses`

Creates a new expense.

Example request:

```json
{
  "date": "2026-09-22",
  "category": "Food",
  "amount": 500,
  "payment_method": "UPI",
  "description": "Lunch"
}
```

The request is validated using the `ExpenseCreate` Pydantic model.

The service then:

1. Reads the existing data
2. Determines the next ID
3. Creates the new record
4. Persists it to the CSV
5. Returns the created expense

---

## PATCH `/expenses/{expense_id}`

Updates only the fields supplied by the client.

Example:

```http
PATCH /expenses/5
```

Request:

```json
{
  "amount": 600
}
```

This demonstrates an important Pydantic capability:

```python
expense.model_dump(exclude_unset=True)
```

Only the fields actually provided by the client are applied to the existing record.

### PUT vs PATCH

This project uses `PATCH` for partial updates.

Conceptually:

```text
PUT
→ Replace the resource

PATCH
→ Modify selected fields
```

---

## DELETE `/expenses/{expense_id}`

Deletes an existing expense.

Example:

```http
DELETE /expenses/5
```

If successful, the API returns a confirmation response.

If the ID does not exist, the API returns HTTP `404`.

---

# 🧩 Pydantic Model Design

The project uses separate models for creation and updates.

### Create model

```python
class ExpenseCreate(BaseModel):
    date: str
    category: str
    amount: float
    payment_method: str
    description: str
```

Creation requires all fields.

### Update model

```python
class ExpenseUpdate(BaseModel):
    date: Optional[str] = None
    category: Optional[str] = None
    amount: Optional[float] = None
    payment_method: Optional[str] = None
    description: Optional[str] = None
```

Update fields are optional because a PATCH request may modify only one field.

For example:

```json
{
  "amount": 600
}
```

Pydantic validates the incoming request before the application logic processes it.

---

# 🧪 Running Tests

Run the complete test suite from the project root:

```bash
python -m pytest
```

The project uses FastAPI's `TestClient` to test API behavior without manually starting the server for each test.

Example:

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
```

The tests demonstrate an important principle:

> A test should validate the expected API contract and behavior, not simply mirror the implementation.

---

# 🔍 HTTP Status Codes Used

| Status | Meaning | Example |
|---|---|---|
| `200` | Successful request | GET /expenses |
| `404` | Resource not found | GET /expenses/999 |
| `422` | Request validation failed | Invalid Pydantic input |

For example, if:

```json
{
  "amount": "invalid"
}
```

is submitted where `amount` is expected to be a number, FastAPI/Pydantic rejects the request with a validation response.

---

# 🧠 Key Learning Concepts

This project demonstrates several foundational concepts that are useful beyond this particular application.

### 1. API Layer

FastAPI turns Python functions into HTTP-accessible endpoints.

```text
HTTP Request
     ↓
FastAPI
     ↓
Python Function
```

### 2. Data Contracts

Pydantic defines the expected shape and types of incoming data.

```text
Client JSON
     ↓
Pydantic validation
     ↓
Validated Python model
```

### 3. Resource-Oriented API Design

The API treats an expense as a resource:

```text
/expenses
/expenses/{id}
```

### 4. CRUD

```text
Create → POST
Read   → GET
Update → PATCH
Delete → DELETE
```

### 5. Persistence

The current implementation persists data to CSV.

This keeps the exercise simple while demonstrating the full request-to-persistence flow.

### 6. Automated Testing

Instead of relying only on Swagger/manual testing:

```text
pytest
   ↓
API request
   ↓
API response
   ↓
assert expected behavior
```

---

# ⚠️ Current Limitations

This project intentionally has several limitations.

### CSV persistence

CSV is useful for learning but is not appropriate as the primary transactional persistence mechanism for a large production API.

For example, with hundreds of millions of records, repeatedly loading and rewriting a complete CSV would be inefficient.

### No authentication

The current API does not implement:

- Authentication
- Authorization
- User-level access control

### No database

There is currently no:

- PostgreSQL
- SQLAlchemy
- NoSQL database
- Managed cloud database

### No production deployment

The service currently runs locally using Uvicorn.

### No service/data-access separation yet

The first iteration keeps the implementation intentionally simple.

These limitations are deliberate because the project is designed as an incremental learning exercise.

---

# 🗺️ Learning Roadmap

The project is intended to evolve through multiple iterations.

## Iteration 1 — API Foundations ✅

```text
FastAPI
Pydantic
REST
CRUD
Validation
Error handling
CSV persistence
Pytest
```

## Iteration 2 — Clean Architecture

Planned improvements:

```text
API Layer
    ↓
Service / Business Layer
    ↓
Repository / Data Layer
    ↓
Persistence
```

Potential topics:

- Separation of concerns
- Dependency injection
- Better project structure
- Configuration management
- More comprehensive testing

## Iteration 3 — Production Engineering

Potential extensions:

```text
Database
Docker
Authentication
Logging
Observability
CI/CD
Cloud deployment
```

## Future AI Integration

The API can eventually become a foundation for AI capabilities such as:

```text
Expense API
     ↓
AI service
     ↓
Categorization
     ↓
Expense insights
     ↓
Natural-language queries
     ↓
Agent / RAG integration
```

This is intentionally outside the scope of the first iteration.

---

# 🎓 What This Project Demonstrates

By completing this project, the learner practices the complete lifecycle of a small API:

```text
Design
  ↓
Implement
  ↓
Validate
  ↓
Persist
  ↓
Test
  ↓
Debug
  ↓
Document
```

The emphasis is not on building a large application. It is on understanding **why each layer exists and what trade-offs appear as the system grows**.

---

# 🤝 Learning & Contribution

This repository is designed to be approachable for developers learning FastAPI and backend/API architecture.

A useful way to work through the project is to:

1. Build the endpoint
2. Test it manually through Swagger
3. Write an automated test
4. Break the implementation intentionally
5. Observe the failure
6. Fix it
7. Think about how the design changes at production scale

Contributions, suggestions, and learning-oriented improvements are welcome.

---

# 📌 Project Status

**Status:** Learning MVP / Iteration 1 complete

The current version focuses on:

- FastAPI fundamentals
- REST API design
- Pydantic validation
- CRUD operations
- CSV persistence
- Automated API testing

Future iterations will progressively introduce cleaner architecture, production persistence, deployment, and AI capabilities.

---

## Author

**Mohit Singh**

AI Architect / Technology Leadership Learning Journey

GitHub: `mohitsingh-analytics`
