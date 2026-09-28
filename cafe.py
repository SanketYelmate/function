
from pathlib import Path
from datetime import datetime
from uuid import uuid4

from flask import Flask, jsonify, request, send_from_directory


BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, static_folder=str(BASE_DIR), static_url_path="")

MENU = {
    "Garden pizza": {"price": 14, "category": "pizza"},
    "Juniper burger": {"price": 12, "category": "burger"},
    "Sunday pasta": {"price": 15, "category": "pasta"},
    "House coffee": {"price": 4, "category": "coffee"},
    "Garden tea": {"price": 4, "category": "tea"},
}


@app.after_request
def add_cors_headers(response):
    if request.path.startswith("/api/"):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response


@app.get("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/api/order", methods=["POST", "OPTIONS"])
def add_order():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}
    item_name = str(data.get("item", "")).strip()
    item = MENU.get(item_name)

    if item is None:
        return jsonify({"error": "That item is not on the menu."}), 400

    return jsonify(
        {
            "message": f"{item_name} added to your order.",
            "item": item_name,
            "price": item["price"],
            "category": item["category"],
        }
    )


@app.route("/api/checkout", methods=["POST", "OPTIONS"])
def checkout():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}
    customer_name = str(data.get("customerName", "")).strip()
    customer_phone = str(data.get("customerPhone", "")).strip()
    cart = data.get("items", [])

    if not customer_name:
        return jsonify({"error": "Please enter your name."}), 400
    if not customer_phone:
        return jsonify({"error": "Please enter your phone number."}), 400
    if not isinstance(cart, list) or not cart:
        return jsonify({"error": "Add at least one item before checkout."}), 400

    bill_items = []
    subtotal = 0
    for cart_item in cart:
        item_name = str(cart_item.get("item", "")).strip()
        quantity = cart_item.get("quantity", 0)
        menu_item = MENU.get(item_name)

        if menu_item is None or not isinstance(quantity, int) or quantity < 1 or quantity > 99:
            return jsonify({"error": "Your cart contains an invalid item or quantity."}), 400

        line_total = menu_item["price"] * quantity
        subtotal += line_total
        bill_items.append(
            {
                "item": item_name,
                "quantity": quantity,
                "unitPrice": menu_item["price"],
                "lineTotal": line_total,
            }
        )

    tax = round(subtotal * 0.05, 2)
    total = round(subtotal + tax, 2)
    invoice_number = f"JUN-{datetime.now():%Y%m%d}-{uuid4().hex[:6].upper()}"

    return jsonify(
        {
            "invoiceNumber": invoice_number,
            "createdAt": datetime.now().strftime("%d %b %Y, %I:%M %p"),
            "customerName": customer_name,
            "customerPhone": customer_phone,
            "items": bill_items,
            "subtotal": subtotal,
            "tax": tax,
            "total": total,
        }
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)

