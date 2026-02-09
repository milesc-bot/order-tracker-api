# Order Tracker API

A RESTful Flask API for managing orders, built following Test-Driven Development (TDD) principles.

## Project Structure

```
backend/
├── __init__.py
├── app.py                  # Flask API routes
├── order_tracker.py        # Core business logic (OrderTracker class)
├── in_memory_storage.py    # In-memory storage backend
└── tests/
    ├── __init__.py
    ├── test_order_tracker.py   # Unit tests for OrderTracker
    └── test_api.py             # Integration tests for API endpoints
```

## Setup

```bash
pip install flask pytest
```

## Running the Server

```bash
python -m backend.app
```

The server starts on `http://0.0.0.0:5000`.

## Running Tests

```bash
pytest
```

## API Reference

### Create Order
```bash
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{"order_id": "ORD001", "items": [{"name": "Widget", "quantity": 2}], "customer_id": "CUST001"}'
```
**Response:** `201 Created`

### Get Order
```bash
curl http://localhost:5000/api/orders/ORD001
```
**Response:** `200 OK`

### Update Order Status
```bash
curl -X PUT http://localhost:5000/api/orders/ORD001 \
  -H "Content-Type: application/json" \
  -d '{"status": "shipped"}'
```
**Response:** `200 OK`

### List All Orders
```bash
curl http://localhost:5000/api/orders
```
**Response:** `200 OK`

### Filter Orders by Status
```bash
curl "http://localhost:5000/api/orders?status=shipped"
```

### Filter Orders by Customer
```bash
curl "http://localhost:5000/api/orders?customer_id=CUST001&status=pending"
```

### Delete Order
```bash
curl -X DELETE http://localhost:5000/api/orders/ORD001
```
**Response:** `200 OK`

## Valid Order Statuses

`pending`, `shipped`, `delivered`, `cancelled`

## Reflection

- **Design Decision — Separation of Concerns:** I separated storage (`InMemoryStorage`), business logic (`OrderTracker`), and the API layer (`app.py`) into distinct modules. This makes it straightforward to swap the in-memory backend for a real database (e.g., PostgreSQL) without touching the API routes or validation logic. The trade-off is a few more files, but the modularity pays off in testability and maintainability.

- **Testing Insight — TDD Caught Validation Gaps:** Writing unit tests before the implementation revealed that early drafts of `add_order` silently accepted zero or negative quantities. A failing test for `quantity=0` prompted adding explicit validation, which the integration tests then confirmed end-to-end. This reinforced the value of the test-first workflow.

- **Next Step — Persistent Storage:** The most impactful improvement would be replacing `InMemoryStorage` with a database-backed implementation (e.g., SQLAlchemy + PostgreSQL). The current architecture already isolates storage behind an interface, so this change would be minimal. Adding status-transition validation (e.g., preventing `delivered → pending`) would also strengthen data integrity.
