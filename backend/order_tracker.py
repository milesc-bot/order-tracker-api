"""
Order Tracker module containing the core business logic for managing orders.

This module provides the OrderTracker class which handles order creation,
retrieval, status updates, and filtering operations.
"""

from backend.in_memory_storage import InMemoryStorage

VALID_STATUSES = {"pending", "shipped", "delivered", "cancelled"}


class OrderTracker:
    """
    Manages orders using an in-memory storage backend.

    Supports creating, retrieving, updating, listing, and filtering orders
    with validation for required fields and status values.
    """

    def __init__(self, storage=None):
        """
        Initialize the OrderTracker with an optional storage backend.

        Args:
            storage: A storage instance. Defaults to InMemoryStorage if not provided.
        """
        self.storage = storage or InMemoryStorage()

    def add_order(self, order_id, items, customer_id):
        """
        Add a new order to the tracker.

        Args:
            order_id (str): Unique identifier for the order.
            items (list): List of item dicts, each with 'name' and 'quantity'.
            customer_id (str): Identifier for the customer placing the order.

        Returns:
            dict: The created order data.

        Raises:
            ValueError: If required fields are missing, invalid, or the ID is a duplicate.
        """
        if not order_id or not isinstance(order_id, str):
            raise ValueError("Order ID is required and must be a non-empty string.")

        if not customer_id or not isinstance(customer_id, str):
            raise ValueError("Customer ID is required and must be a non-empty string.")

        if not items or not isinstance(items, list):
            raise ValueError("Items must be a non-empty list.")

        for item in items:
            if not isinstance(item, dict):
                raise ValueError("Each item must be a dictionary.")
            if "name" not in item or "quantity" not in item:
                raise ValueError("Each item must have 'name' and 'quantity' fields.")
            if not isinstance(item["quantity"], int) or item["quantity"] <= 0:
                raise ValueError("Item quantity must be a positive integer.")

        if self.storage.exists(order_id):
            raise ValueError(f"Order with ID '{order_id}' already exists.")

        order = {
            "order_id": order_id,
            "items": items,
            "customer_id": customer_id,
            "status": "pending",
        }
        self.storage.save(order_id, order)
        return order

    def get_order_by_id(self, order_id):
        """
        Retrieve an order by its ID.

        Args:
            order_id (str): The unique identifier of the order to retrieve.

        Returns:
            dict: The order data.

        Raises:
            ValueError: If the order ID is empty or not a string.
            KeyError: If no order is found with the given ID.
        """
        if not order_id or not isinstance(order_id, str):
            raise ValueError("Order ID must be a non-empty string.")

        order = self.storage.get(order_id)
        if order is None:
            raise KeyError(f"Order with ID '{order_id}' not found.")
        return order

    def update_order_status(self, order_id, new_status):
        """
        Update the status of an existing order.

        Args:
            order_id (str): The unique identifier of the order to update.
            new_status (str): The new status value.

        Returns:
            dict: The updated order data.

        Raises:
            ValueError: If the order ID is empty or the status is invalid.
            KeyError: If no order is found with the given ID.
        """
        if not order_id or not isinstance(order_id, str):
            raise ValueError("Order ID must be a non-empty string.")

        if new_status not in VALID_STATUSES:
            raise ValueError(
                f"Invalid status '{new_status}'. Must be one of: {', '.join(sorted(VALID_STATUSES))}."
            )

        order = self.storage.get(order_id)
        if order is None:
            raise KeyError(f"Order with ID '{order_id}' not found.")

        order["status"] = new_status
        self.storage.save(order_id, order)
        return order

    def list_all_orders(self):
        """
        List all orders in the tracker.

        Returns:
            list: A list of all order data dictionaries.
        """
        return self.storage.get_all()

    def list_orders_by_status(self, status):
        """
        List orders filtered by a specific status.

        Args:
            status (str): The status to filter by.

        Returns:
            list: A list of orders matching the given status.

        Raises:
            ValueError: If the status value is invalid.
        """
        if status not in VALID_STATUSES:
            raise ValueError(
                f"Invalid status '{status}'. Must be one of: {', '.join(sorted(VALID_STATUSES))}."
            )

        return [order for order in self.storage.get_all() if order["status"] == status]
