from datetime import datetime

def calculate_monthly_limit(user):
    return user["salary"] - user["expenses"] - user["emi"]


def calculate_food_spend(transactions):
    return sum(
        t["amount"] for t in transactions
        if t["category"] == "Food Delivery"
    )


def calculate_addiction_score(transactions):
    if not transactions:
        return 0

    food_transactions = [
        t for t in transactions
        if t["category"] == "Food Delivery"
    ]

    frequency_score = min(len(food_transactions) * 5, 40)

    amount_score = min(
        sum(t["amount"] for t in food_transactions) / 100,
        40
    )

    late_night_score = 0
    for t in food_transactions:
        hour = t.get("hour", 12)
        if hour >= 22 or hour <= 5:
            late_night_score += 5

    late_night_score = min(late_night_score, 20)

    return int(frequency_score + amount_score + late_night_score)