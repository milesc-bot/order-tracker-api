"""
Unit tests for the OrderTracker class.

Tests cover order creation, retrieval, status updates,
listing, and filtering, including edge cases and invalid inputs.
"""

import pytest
from backend.order_tracker import OrderTracker


@pytest.fixture
def tracker():
    """Provide a fresh OrderTracker instance for each test."""
    return OrderTracker()


@pytest.fixture
def sample_order(tracker):
    """Add and return a sample order for tests that need existing data."""
    return tracker.add_order(
        order_id="ORD001",
        items=[{"name": "Widget", "quantity": 2}],
        customer_id="CUST001",
    )


# ── Order Creation Tests ──────────────────────────────────────────────


class TestAddOrder:
    """Tests for the add_order method."""

    def test_add_order_success(self, tracker):
        """A new order is stored with correct details and defaults to 'pending'."""
        order = tracker.add_order(
            order_id="ORD001",
            items=[{"name": "Widget", "quantity": 3}],
            customer_id="CUST001",
        )
        assert order["order_id"] == "ORD001"
        assert order["customer_id"] == "CUST001"
        assert order["items"] == [{"name": "Widget", "quantity": 3}]
        assert order["status"] == "pending"

    def test_add_order_multiple_items(self, tracker):
        """An order can contain multiple items."""
        items = [
            {"name": "Widget", "quantity": 1},
            {"name": "Gadget", "quantity": 5},
        ]
        order = tracker.add_order("ORD002", items, "CUST002")
        assert len(order["items"]) == 2

    def test_add_order_duplicate_id_raises(self, tracker, sample_order):
        """Adding an order with a duplicate ID raises ValueError."""
        with pytest.raises(ValueError, match="already exists"):
            tracker.add_order(
                "ORD001",
                [{"name": "Gadget", "quantity": 1}],
                "CUST002",
            )

    def test_add_order_missing_order_id(self, tracker):
        """An empty or None order ID raises ValueError."""
        with pytest.raises(ValueError, match="Order ID is required"):
            tracker.add_order("", [{"name": "Widget", "quantity": 1}], "CUST001")

    def test_add_order_none_order_id(self, tracker):
        """A None order ID raises ValueError."""
        with pytest.raises(ValueError, match="Order ID is required"):
            tracker.add_order(None, [{"name": "Widget", "quantity": 1}], "CUST001")

    def test_add_order_missing_customer_id(self, tracker):
        """An empty customer ID raises ValueError."""
        with pytest.raises(ValueError, match="Customer ID is required"):
            tracker.add_order("ORD001", [{"name": "Widget", "quantity": 1}], "")

    def test_add_order_empty_items(self, tracker):
        """An empty items list raises ValueError."""
        with pytest.raises(ValueError, match="Items must be a non-empty list"):
            tracker.add_order("ORD001", [], "CUST001")

    def test_add_order_invalid_quantity(self, tracker):
        """A non-positive item quantity raises ValueError."""
        with pytest.raises(ValueError, match="quantity must be a positive integer"):
            tracker.add_order("ORD001", [{"name": "Widget", "quantity": 0}], "CUST001")

    def test_add_order_negative_quantity(self, tracker):
        """A negative item quantity raises ValueError."""
        with pytest.raises(ValueError, match="quantity must be a positive integer"):
            tracker.add_order(
                "ORD001", [{"name": "Widget", "quantity": -1}], "CUST001"
            )

    def test_add_order_item_missing_fields(self, tracker):
        """An item dict without 'name' or 'quantity' raises ValueError."""
        with pytest.raises(ValueError, match="must have 'name' and 'quantity'"):
            tracker.add_order("ORD001", [{"name": "Widget"}], "CUST001")


# ── Order Retrieval Tests ─────────────────────────────────────────────


class TestGetOrderById:
    """Tests for the get_order_by_id method."""

    def test_get_existing_order(self, tracker, sample_order):
        """Retrieving an existing order returns the correct data."""
        order = tracker.get_order_by_id("ORD001")
        assert order["order_id"] == "ORD001"
        assert order["customer_id"] == "CUST001"
        assert order["status"] == "pending"

    def test_get_nonexistent_order_raises(self, tracker):
        """Fetching a non-existent order raises KeyError."""
        with pytest.raises(KeyError, match="not found"):
            tracker.get_order_by_id("MISSING")

    def test_get_order_empty_id_raises(self, tracker):
        """An empty order ID raises ValueError."""
        with pytest.raises(ValueError, match="non-empty string"):
            tracker.get_order_by_id("")

    def test_get_order_none_id_raises(self, tracker):
        """A None order ID raises ValueError."""
        with pytest.raises(ValueError, match="non-empty string"):
            tracker.get_order_by_id(None)


# ── Order Status Update Tests ─────────────────────────────────────────


class TestUpdateOrderStatus:
    """Tests for the update_order_status method."""

    def test_update_status_success(self, tracker, sample_order):
        """Updating status from 'pending' to 'shipped' works correctly."""
        updated = tracker.update_order_status("ORD001", "shipped")
        assert updated["status"] == "shipped"

    def test_update_status_to_delivered(self, tracker, sample_order):
        """Updating status to 'delivered' works correctly."""
        updated = tracker.update_order_status("ORD001", "delivered")
        assert updated["status"] == "delivered"

    def test_update_status_to_cancelled(self, tracker, sample_order):
        """Updating status to 'cancelled' works correctly."""
        updated = tracker.update_order_status("ORD001", "cancelled")
        assert updated["status"] == "cancelled"

    def test_update_status_invalid_raises(self, tracker, sample_order):
        """An invalid status value raises ValueError."""
        with pytest.raises(ValueError, match="Invalid status"):
            tracker.update_order_status("ORD001", "flying")

    def test_update_status_nonexistent_order_raises(self, tracker):
        """Updating a non-existent order raises KeyError."""
        with pytest.raises(KeyError, match="not found"):
            tracker.update_order_status("MISSING", "shipped")

    def test_update_status_empty_id_raises(self, tracker):
        """An empty order ID raises ValueError."""
        with pytest.raises(ValueError, match="non-empty string"):
            tracker.update_order_status("", "shipped")

    def test_update_status_persists(self, tracker, sample_order):
        """Updated status is reflected on subsequent retrieval."""
        tracker.update_order_status("ORD001", "shipped")
        order = tracker.get_order_by_id("ORD001")
        assert order["status"] == "shipped"


# ── List and Filter Tests ─────────────────────────────────────────────


class TestListOrders:
    """Tests for list_all_orders and list_orders_by_status methods."""

    def test_list_all_orders_empty(self, tracker):
        """Listing all orders when none exist returns an empty list."""
        assert tracker.list_all_orders() == []

    def test_list_all_orders(self, tracker):
        """Listing all orders returns every order in the tracker."""
        tracker.add_order("ORD001", [{"name": "A", "quantity": 1}], "C1")
        tracker.add_order("ORD002", [{"name": "B", "quantity": 2}], "C2")
        tracker.add_order("ORD003", [{"name": "C", "quantity": 3}], "C3")
        orders = tracker.list_all_orders()
        assert len(orders) == 3
        ids = {o["order_id"] for o in orders}
        assert ids == {"ORD001", "ORD002", "ORD003"}

    def test_list_orders_by_status(self, tracker):
        """Filtering by status returns only matching orders."""
        tracker.add_order("ORD001", [{"name": "A", "quantity": 1}], "C1")
        tracker.add_order("ORD002", [{"name": "B", "quantity": 2}], "C2")
        tracker.update_order_status("ORD002", "shipped")
        shipped = tracker.list_orders_by_status("shipped")
        assert len(shipped) == 1
        assert shipped[0]["order_id"] == "ORD002"

    def test_list_orders_by_status_no_match(self, tracker, sample_order):
        """Filtering by a status with no matches returns an empty list."""
        result = tracker.list_orders_by_status("delivered")
        assert result == []

    def test_list_orders_by_invalid_status_raises(self, tracker):
        """Filtering by an invalid status raises ValueError."""
        with pytest.raises(ValueError, match="Invalid status"):
            tracker.list_orders_by_status("unknown")

    def test_list_orders_by_status_pending(self, tracker):
        """Filtering by 'pending' returns only pending orders."""
        tracker.add_order("ORD001", [{"name": "A", "quantity": 1}], "C1")
        tracker.add_order("ORD002", [{"name": "B", "quantity": 2}], "C2")
        tracker.update_order_status("ORD001", "shipped")
        pending = tracker.list_orders_by_status("pending")
        assert len(pending) == 1
        assert pending[0]["order_id"] == "ORD002"
