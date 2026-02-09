"""
Integration tests for the Flask API endpoints.

Tests cover creating, retrieving, updating, listing, and deleting orders
through the REST API, verifying correct HTTP status codes and JSON responses.
"""

import pytest
from backend.app import app, tracker


@pytest.fixture(autouse=True)
def reset_storage():
    """Clear storage before each test for isolation."""
    tracker.storage.clear()
    yield


@pytest.fixture
def client():
    """Provide a Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ── POST /api/orders ──────────────────────────────────────────────────


class TestCreateOrderEndpoint:
    """Tests for the POST /api/orders endpoint."""

    def test_create_order_success(self, client):
        """POST with valid data returns 201 and the order JSON."""
        payload = {
            "order_id": "ORD100",
            "items": [{"name": "Widget", "quantity": 2}],
            "customer_id": "CUST100",
        }
        response = client.post("/api/orders", json=payload)
        assert response.status_code == 201
        data = response.get_json()
        assert data["order_id"] == "ORD100"
        assert data["status"] == "pending"
        assert data["customer_id"] == "CUST100"

    def test_create_order_missing_fields(self, client):
        """POST with missing fields returns 400."""
        response = client.post("/api/orders", json={"order_id": "ORD101"})
        assert response.status_code == 400
        assert "error" in response.get_json()

    def test_create_order_duplicate_id(self, client):
        """POST with a duplicate order ID returns 400."""
        payload = {
            "order_id": "ORD100",
            "items": [{"name": "Widget", "quantity": 1}],
            "customer_id": "CUST100",
        }
        client.post("/api/orders", json=payload)
        response = client.post("/api/orders", json=payload)
        assert response.status_code == 400
        assert "error" in response.get_json()


# ── GET /api/orders/<order_id> ────────────────────────────────────────


class TestGetOrderEndpoint:
    """Tests for the GET /api/orders/<order_id> endpoint."""

    def test_get_order_success(self, client):
        """GET for an existing order returns 200 and the correct JSON."""
        payload = {
            "order_id": "ORD200",
            "items": [{"name": "Gadget", "quantity": 1}],
            "customer_id": "CUST200",
        }
        client.post("/api/orders", json=payload)
        response = client.get("/api/orders/ORD200")
        assert response.status_code == 200
        data = response.get_json()
        assert data["order_id"] == "ORD200"
        assert data["customer_id"] == "CUST200"

    def test_get_order_not_found(self, client):
        """GET for a non-existent order returns 404."""
        response = client.get("/api/orders/NONEXISTENT")
        assert response.status_code == 404
        assert "error" in response.get_json()


# ── PUT /api/orders/<order_id> ────────────────────────────────────────


class TestUpdateOrderEndpoint:
    """Tests for the PUT /api/orders/<order_id> endpoint."""

    def test_update_order_status_success(self, client):
        """PUT with a valid status returns 200 and the updated JSON."""
        payload = {
            "order_id": "ORD300",
            "items": [{"name": "Gizmo", "quantity": 4}],
            "customer_id": "CUST300",
        }
        client.post("/api/orders", json=payload)
        response = client.put("/api/orders/ORD300", json={"status": "shipped"})
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "shipped"

    def test_update_order_invalid_status(self, client):
        """PUT with an invalid status returns 400."""
        payload = {
            "order_id": "ORD300",
            "items": [{"name": "Gizmo", "quantity": 4}],
            "customer_id": "CUST300",
        }
        client.post("/api/orders", json=payload)
        response = client.put("/api/orders/ORD300", json={"status": "flying"})
        assert response.status_code == 400
        assert "error" in response.get_json()

    def test_update_order_not_found(self, client):
        """PUT for a non-existent order returns 404."""
        response = client.put("/api/orders/MISSING", json={"status": "shipped"})
        assert response.status_code == 404
        assert "error" in response.get_json()


# ── GET /api/orders ───────────────────────────────────────────────────


class TestListOrdersEndpoint:
    """Tests for the GET /api/orders endpoint."""

    def test_list_all_orders(self, client):
        """GET /api/orders returns 200 and includes all created orders."""
        client.post(
            "/api/orders",
            json={
                "order_id": "ORD400",
                "items": [{"name": "A", "quantity": 1}],
                "customer_id": "C1",
            },
        )
        client.post(
            "/api/orders",
            json={
                "order_id": "ORD401",
                "items": [{"name": "B", "quantity": 2}],
                "customer_id": "C2",
            },
        )
        response = client.get("/api/orders")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) >= 2
        ids = [o["order_id"] for o in data]
        assert "ORD400" in ids
        assert "ORD401" in ids

    def test_list_orders_filtered_by_status(self, client):
        """GET /api/orders?status=shipped returns only shipped orders."""
        client.post(
            "/api/orders",
            json={
                "order_id": "ORD500",
                "items": [{"name": "X", "quantity": 1}],
                "customer_id": "C1",
            },
        )
        client.post(
            "/api/orders",
            json={
                "order_id": "ORD501",
                "items": [{"name": "Y", "quantity": 1}],
                "customer_id": "C2",
            },
        )
        client.put("/api/orders/ORD501", json={"status": "shipped"})
        response = client.get("/api/orders?status=shipped")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]["order_id"] == "ORD501"

    def test_list_orders_filtered_by_customer(self, client):
        """GET /api/orders?customer_id=C1 returns only that customer's orders."""
        client.post(
            "/api/orders",
            json={
                "order_id": "ORD600",
                "items": [{"name": "M", "quantity": 1}],
                "customer_id": "C1",
            },
        )
        client.post(
            "/api/orders",
            json={
                "order_id": "ORD601",
                "items": [{"name": "N", "quantity": 1}],
                "customer_id": "C2",
            },
        )
        response = client.get("/api/orders?customer_id=C1")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]["customer_id"] == "C1"


# ── DELETE /api/orders/<order_id> ─────────────────────────────────────


class TestDeleteOrderEndpoint:
    """Tests for the DELETE /api/orders/<order_id> endpoint."""

    def test_delete_order_success(self, client):
        """DELETE for an existing order returns 200 and the deleted order."""
        payload = {
            "order_id": "ORD700",
            "items": [{"name": "Z", "quantity": 1}],
            "customer_id": "CUST700",
        }
        client.post("/api/orders", json=payload)
        response = client.delete("/api/orders/ORD700")
        assert response.status_code == 200
        assert response.get_json()["order_id"] == "ORD700"
        get_resp = client.get("/api/orders/ORD700")
        assert get_resp.status_code == 404

    def test_delete_order_not_found(self, client):
        """DELETE for a non-existent order returns 404."""
        response = client.delete("/api/orders/GHOST")
        assert response.status_code == 404
        assert "error" in response.get_json()
