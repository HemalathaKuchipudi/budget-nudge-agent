import pandas as pd

def calculate_addiction_score(df, monthly_limit):

    food_df = df[df["category"] == "Food Delivery"]

    if len(food_df) == 0:
        return 0

    total_orders = len(food_df)
    total_spent = food_df["amount"].sum()

    # ---- FREQUENCY SCORE (max 40)
    # 20+ orders = full 40
    frequency_score = min((total_orders / 20) * 40, 40)

    # ---- AMOUNT SCORE (max 40)
    amount_ratio = total_spent / monthly_limit if monthly_limit > 0 else 0
    amount_score = min(amount_ratio * 40, 40)

    # ---- LATE NIGHT SCORE (max 20)
    late_night_orders = food_df[
        food_df["time"].apply(is_late_night)
    ]

    late_ratio = len(late_night_orders) / total_orders
    late_score = late_ratio * 20

    total_score = int(frequency_score + amount_score + late_score)

    return min(total_score, 100)


def is_late_night(time_str):
    try:
        hour = int(time_str.split(":")[0])
        return hour >= 22 or hour <= 4
    except:
        return False