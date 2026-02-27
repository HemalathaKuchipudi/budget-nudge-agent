def generate_nudge(spend, threshold, personality):
    if personality == "Savage":
        return f"₹{spend}? At this rate Swiggy should give you loyalty shares."
    elif personality == "Friendly":
        return f"You spent ₹{spend}. Maybe cook once this week?"
    else:
        return f"You're over budget by ₹{spend - threshold}."