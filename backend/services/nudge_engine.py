def generate_static_llm_nudge(monthly_limit, food_spend, addiction_score, transactions):

    total_spend = sum(tx["amount"] for tx in transactions)

    # Budget usage %
    usage_percent = (total_spend / monthly_limit) * 100 if monthly_limit > 0 else 0

    # Food dominance %
    food_ratio = (food_spend / total_spend) * 100 if total_spend > 0 else 0

    # Late night orders
    late_orders = sum(1 for tx in transactions if tx["hour"] >= 23 or tx["hour"] <= 5)
    late_ratio = (late_orders / len(transactions)) if transactions else 0

    # ---- Smart Static "LLM style" responses ----

    if usage_percent > 90:
        return f"🚨 You’ve used {usage_percent:.0f}% of your budget. Your wallet is sweating!"

    if addiction_score > 70:
        return "🍔 Food delivery seems to be your best friend lately. Maybe give your kitchen a chance?"

    if food_ratio > 50:
        return "📦 More than half your spending is on food delivery. Chef mode ON this week?"

    if late_ratio > 0.4:
        return "🌙 Late-night spending detected. Midnight cravings cost more than you think!"

    if usage_percent > 70:
        return "⚠ You are nearing your spending limit. Slow and steady wins the month."

    return "👏 You're managing your finances well. Keep it up!"