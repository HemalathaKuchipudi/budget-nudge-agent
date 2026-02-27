from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

from storage import users, transactions
from services.calculations import (
    calculate_monthly_limit,
    calculate_food_spend,
    calculate_addiction_score
)

from services.nudge_engine import generate_static_llm_nudge

app = Flask(__name__)
CORS(app)


# -----------------------
# Create User
# -----------------------
@app.route("/create-user", methods=["POST"])
def create_user():
    data = request.json

    user_id = data["name"].replace(" ", "_")

    users[user_id] = {
        "salary": float(data["salary"]),
        "expenses": float(data["expenses"]),
        "emi": float(data["emi"])
    }

    transactions[user_id] = []

    return jsonify({"user_id": user_id})


# -----------------------
# Add Transaction
# -----------------------
@app.route("/add-transaction/<user_id>", methods=["POST"])
def add_transaction(user_id):
    data = request.json

    new_transaction = {
        "merchant": data["merchant"],
        "amount": float(data["amount"]),
        "category": data["category"],
        "hour": datetime.now().hour
    }

    transactions[user_id].append(new_transaction)

    return jsonify({"message": "Transaction added"})


# -----------------------
# Dashboard Data
# -----------------------
@app.route("/dashboard/<user_id>")
def dashboard(user_id):

    user = users.get(user_id)
    user_transactions = transactions.get(user_id, [])

    monthly_limit = calculate_monthly_limit(user)
    food_spend = calculate_food_spend(user_transactions)
    addiction_score = calculate_addiction_score(user_transactions)

    # 🔥 Generate Static LLM-style Nudge
    nudge = generate_static_llm_nudge(
        monthly_limit,
        food_spend,
        addiction_score,
        user_transactions
    )

    return jsonify({
        "monthly_limit": monthly_limit,
        "food_spend": food_spend,
        "addiction_score": addiction_score,
        "transactions": user_transactions,
        "nudge": nudge
    })


if __name__ == "__main__":
    app.run(debug=True)