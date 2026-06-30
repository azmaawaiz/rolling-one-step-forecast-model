import pandas as pd

# ==========================================================
# Initial training dataset (ONLY up to September 2021)
# ==========================================================
data = {
    'Date': [
        '10/31/20', '11/30/20', '12/31/20',
        '1/31/21', '2/28/21', '3/31/21',
        '4/30/21', '5/31/21', '6/30/21',
        '7/31/21', '8/31/21', '9/30/21'
    ],
    'Price': [
        10.10, 10.30, 11.00,
        10.90, 10.90, 10.90,
        10.40, 9.84, 10.00,
        10.10, 10.30, 10.20
    ]
}

df = pd.DataFrame(data)
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")
df["Month"] = df["Date"].dt.month

# ==========================================================
# Actual historical prices (used AFTER each prediction)
# ==========================================================
actual_prices = {
    '2021-10-31': 10.10,
    '2021-11-30': 11.20,
    '2021-12-31': 11.40,
    '2022-01-31': 11.50,
    '2022-02-28': 11.80,
    '2022-03-31': 11.50,
    '2022-04-30': 10.70,
    '2022-05-31': 10.70,
    '2022-06-30': 10.40,
    '2022-07-31': 10.50,
    '2022-08-31': 10.40,
    '2022-09-30': 10.80,
    '2022-10-31': 11.00,
    '2022-11-30': 11.60,
    '2022-12-31': 11.60,
    '2023-01-31': 12.10,
    '2023-02-28': 11.70,
    '2023-03-31': 12.00,
    '2023-04-30': 11.50,
    '2023-05-31': 11.20,
    '2023-06-30': 10.90,
    '2023-07-31': 11.40,
    '2023-08-31': 11.10,
    '2023-09-30': 11.50,
    '2023-10-31': 11.80,
    '2023-11-30': 12.20,
    '2023-12-31': 12.80,
    '2024-01-31': 12.60,
    '2024-02-29': 12.40,
    '2024-03-31': 12.70,
    '2024-04-30': 12.10,
    '2024-05-31': 11.40,
    '2024-06-30': 11.50,
    '2024-07-31': 11.60,
    '2024-08-31': 11.50,
    '2024-09-30': 11.80
}

# ==========================================================
# Seasonal groups
# ==========================================================
decreasing_months = [12, 1, 2, 3, 4, 5]
increasing_months = [5, 6, 7, 8, 9, 10, 11, 12]

# ==========================================================
# Forecast period
# ==========================================================
start_target_date = pd.to_datetime("2021-10-31")
end_target_date = pd.to_datetime("2024-09-30")

current_date = start_target_date

predictions = []

print("\n===============================")
print("ROLLING % CHANGE FORECAST")
print("===============================\n")

while current_date <= end_target_date:

    # --------------------------------------
    # Calculate percentage changes
    # --------------------------------------
    df = df.sort_values("Date").reset_index(drop=True)

    df["Pct_Change"] = df["Price"].pct_change()

    decreasing_data = df[df["Month"].isin(decreasing_months)]
    increasing_data = df[df["Month"].isin(increasing_months)]

    decreasing_pct = decreasing_data["Pct_Change"].dropna().mean()
    increasing_pct = increasing_data["Pct_Change"].dropna().mean()
    overall_pct = df["Pct_Change"].dropna().mean()

    target_month = current_date.month

    # --------------------------------------
    # Seasonal logic (same as before)
    # --------------------------------------
    if target_month in [6, 7, 8, 9, 10, 11]:

        expected_change = (
            increasing_pct +
            overall_pct
        ) / 2

        logic = "Increasing Group"

    elif target_month in [1, 2, 3, 4]:

        expected_change = (
            decreasing_pct +
            overall_pct
        ) / 2

        logic = "Decreasing Group"

    else:

        expected_change = (
            increasing_pct +
            decreasing_pct +
            overall_pct
        ) / 3

        logic = "Overlap"

    # --------------------------------------
    # Forecast using LAST ACTUAL price
    # --------------------------------------
    last_actual = df.iloc[-1]["Price"]

    predicted_price = last_actual * (1 + expected_change)

    actual_price = actual_prices[current_date.strftime("%Y-%m-%d")]

    predictions.append({
        "Date": current_date.strftime("%m/%d/%Y"),
        "Prediction": round(predicted_price, 2),
        "Actual": actual_price,
        "Expected % Change": round(expected_change * 100, 2),
        "Error": round(actual_price - predicted_price, 2)
    })

    print(f"{current_date.strftime('%m/%d/%Y')}")
    print(f"Logic Used          : {logic}")
    print(f"Last Actual Price   : £{last_actual:.2f}")
    print(f"Increasing Avg %    : {increasing_pct*100:.2f}%")
    print(f"Decreasing Avg %    : {decreasing_pct*100:.2f}%")
    print(f"Overall Avg %       : {overall_pct*100:.2f}%")
    print(f"Expected % Change   : {expected_change*100:.2f}%")
    print(f"Prediction          : £{predicted_price:.2f}")
    print(f"Actual              : £{actual_price:.2f}")
    print("-" * 55)

    # --------------------------------------
    # Add the ACTUAL value for next iteration
    # --------------------------------------
    new_row = pd.DataFrame({
        "Date": [current_date],
        "Price": [actual_price],
        "Month": [target_month]
    })

    df = pd.concat([df, new_row], ignore_index=True)

    current_date += pd.offsets.MonthEnd(1)

# ==========================================================
# Results
# ==========================================================
predictions_df = pd.DataFrame(predictions)

print("\n===============================")
print("FINAL PREDICTIONS")
print("===============================\n")

print(predictions_df)

