# Order Tracker API

## Overview
A backend-only RESTful Flask API for managing orders, built following Test-Driven Development (TDD) principles. No UI/UX or frontend — purely a backend service with comprehensive tests.

## Project Architecture
```
backend/
├── __init__.py
├── app.py                  # Flask API routes (POST, GET, PUT, DELETE)
├── order_tracker.py        # Core business logic (OrderTracker class)
├── in_memory_storage.py    # Dictionary-based in-memory storage
└── tests/
    ├── __init__.py
    ├── test_order_tracker.py   # 27 unit tests for OrderTracker
    └── test_api.py             # 13 integration tests for API endpoints
starter/
└── README.md               # Project documentation with reflection
```

## Key Decisions
- Three-layer separation: storage, business logic, API
- In-memory storage for simplicity (swappable for DB later)
- Valid statuses: pending, shipped, delivered, cancelled
- Consistent JSON error responses with appropriate HTTP status codes

## Recent Changes
- 2026-02-09: Initial project creation with all core features
- 2026-02-09: Pushed to GitHub at https://github.com/milesc-bot/order-tracker-api

## Running Tests
```bash
python -m pytest -v
```

## Dependencies
- Flask (web framework)
- pytest (testing)
