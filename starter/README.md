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

- **Design trade-off:** I split the project into three layers — storage, business logic, and API — so each can change independently. The trade-off is more files, but it makes swapping in a real database later a one-file change instead of a rewrite.
- **Testing insight:** A unit test for `quantity=0` exposed that my initial `add_order` silently accepted invalid quantities. That failing test drove me to add explicit validation before any order is stored, which the integration tests then confirmed end-to-end.
- **Next-step improvement:** I would replace `InMemoryStorage` with a database-backed implementation (e.g., SQLAlchemy + PostgreSQL) and add status-transition rules to prevent illogical changes like moving from `delivered` back to `pending`.
