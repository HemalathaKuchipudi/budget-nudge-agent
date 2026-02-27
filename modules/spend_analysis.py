def calculate_food_spend(df):
    if df is None:
        return 0

    food_merchants = ["Swiggy", "Zomato"]

    food_df = df[df["merchant"].isin(food_merchants)]
    total = food_df["amount"].sum()

    return total