"""
Flask API module for the Order Tracker application.

Provides RESTful endpoints for creating, retrieving, updating,
and listing orders.
"""

from flask import Flask, jsonify, request
from backend.order_tracker import OrderTracker

app = Flask(__name__)
tracker = OrderTracker()


@app.errorhandler(400)
def bad_request(error):
    """Handle 400 Bad Request errors."""
    return jsonify({"error": str(error.description)}), 400


@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors."""
    return jsonify({"error": str(error.description)}), 404


@app.route("/api/orders", methods=["POST"])
def create_order():
    """
    Create a new order.

    Expects JSON body with 'order_id', 'items', and 'customer_id'.
    Returns 201 Created with the order JSON on success.
    Returns 400 Bad Request for validation errors.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    order_id = data.get("order_id")
    items = data.get("items")
    customer_id = data.get("customer_id")

    try:
        order = tracker.add_order(order_id, items, customer_id)
        return jsonify(order), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/orders/<order_id>", methods=["GET"])
def get_order(order_id):
    """
    Retrieve a single order by its ID.

    Returns 200 OK with the order JSON on success.
    Returns 404 Not Found if the order does not exist.
    """
    try:
        order = tracker.get_order_by_id(order_id)
        return jsonify(order), 200
    except (ValueError, KeyError) as e:
        return jsonify({"error": str(e)}), 404


@app.route("/api/orders/<order_id>", methods=["PUT"])
def update_order(order_id):
    """
    Update the status of an existing order.

    Expects JSON body with 'status'.
    Returns 200 OK with the updated order JSON on success.
    Returns 400 Bad Request for invalid status values.
    Returns 404 Not Found if the order does not exist.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    new_status = data.get("status")
    if not new_status:
        return jsonify({"error": "Missing 'status' field in request body."}), 400

    try:
        order = tracker.update_order_status(order_id, new_status)
        return jsonify(order), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except KeyError as e:
        return jsonify({"error": str(e)}), 404


@app.route("/api/orders", methods=["GET"])
def list_orders():
    """
    List all orders, optionally filtered by status and/or customer_id.

    Query parameters:
        status (str, optional): Filter by order status.
        customer_id (str, optional): Filter by customer ID.

    Returns 200 OK with a JSON list of orders.
    Returns 400 Bad Request for invalid status filter values.
    """
    status = request.args.get("status")
    customer_id = request.args.get("customer_id")

    try:
        if status:
            orders = tracker.list_orders_by_status(status)
        else:
            orders = tracker.list_all_orders()

        if customer_id:
            orders = [o for o in orders if o["customer_id"] == customer_id]

        return jsonify(orders), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/orders/<order_id>", methods=["DELETE"])
def delete_order(order_id):
    """
    Delete an order by its ID.

    Returns 200 OK with the deleted order JSON on success.
    Returns 404 Not Found if the order does not exist.
    """
    try:
        order = tracker.get_order_by_id(order_id)
        tracker.storage.delete(order_id)
        return jsonify(order), 200
    except (ValueError, KeyError) as e:
        return jsonify({"error": str(e)}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
