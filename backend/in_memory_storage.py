"""
In-memory storage module for the Order Tracker application.

Provides a simple dictionary-based storage mechanism for orders,
suitable for development and testing purposes.
"""


class InMemoryStorage:
    """A simple in-memory storage backend using a Python dictionary."""

    def __init__(self):
        """Initialize an empty storage dictionary."""
        self._orders = {}

    def save(self, order_id, order_data):
        """
        Save an order to storage.

        Args:
            order_id (str): The unique identifier for the order.
            order_data (dict): The order data to store.
        """
        self._orders[order_id] = order_data

    def get(self, order_id):
        """
        Retrieve an order by its ID.

        Args:
            order_id (str): The unique identifier for the order.

        Returns:
            dict or None: The order data if found, None otherwise.
        """
        return self._orders.get(order_id)

    def get_all(self):
        """
        Retrieve all stored orders.

        Returns:
            list: A list of all order data dictionaries.
        """
        return list(self._orders.values())

    def exists(self, order_id):
        """
        Check if an order exists in storage.

        Args:
            order_id (str): The unique identifier to check.

        Returns:
            bool: True if the order exists, False otherwise.
        """
        return order_id in self._orders

    def delete(self, order_id):
        """
        Delete an order from storage.

        Args:
            order_id (str): The unique identifier for the order to delete.

        Returns:
            dict or None: The deleted order data if found, None otherwise.
        """
        return self._orders.pop(order_id, None)

    def clear(self):
        """Remove all orders from storage."""
        self._orders.clear()
