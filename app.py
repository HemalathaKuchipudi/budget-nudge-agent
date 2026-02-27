from modules.data_loader import load_transactions
from modules.spend_analysis import calculate_food_spend
from modules.nudge_generator import generate_nudge
import config


def main():
    print("=== Budget Nudge Agent ===")

    df = load_transactions(config.CSV_PATH)

    total_food_spend = calculate_food_spend(df)

    print(f"Total Food Delivery Spend: ₹{total_food_spend}")

    if total_food_spend > config.FOOD_THRESHOLD:
        nudge = generate_nudge(
            spend=total_food_spend,
            threshold=config.FOOD_THRESHOLD,
            personality=config.PERSONALITY_MODE
        )
        print("⚠ Overspending Detected!")
        print("AI Nudge:", nudge)
    else:
        print("You're within budget. Great job!")


if __name__ == "__main__":
    main()