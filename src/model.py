import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import mean_absolute_error


def build_waking_pairs(df):
    df = df.copy().sort_values("timestamp").reset_index(drop=True)

    bedtime_rows = df[df["meal_context"] == "bedtime"][["timestamp", "lantus_units"]].copy()
    waking_rows = df[df["waking_reading"] == 1][["timestamp", "glucose_mg_dl"]].copy().reset_index(drop=True)

    pairs = []
    for _, brow in bedtime_rows.iterrows():
        prev_waking = waking_rows[waking_rows["timestamp"] < brow["timestamp"]]
        future_waking = waking_rows[waking_rows["timestamp"] > brow["timestamp"]]

        if prev_waking.empty or future_waking.empty:
            continue

        last_waking = prev_waking.iloc[-1]
        next_waking = future_waking.iloc[0]

        pairs.append({
            "lantus_units": brow["lantus_units"],
            "prev_waking_glucose": last_waking["glucose_mg_dl"],
            "next_waking_glucose": next_waking["glucose_mg_dl"],
        })

    return pd.DataFrame(pairs)


def train_and_evaluate(pairs):
    X = pairs[["lantus_units", "prev_waking_glucose"]].values
    y = pairs["next_waking_glucose"].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = Ridge(alpha=1.0)

    loo = LeaveOneOut()
    predictions = []
    actuals = []

    for train_index, test_index in loo.split(X_scaled):
        X_train, X_test = X_scaled[train_index], X_scaled[test_index]
        y_train, y_test = y[train_index], y[test_index]

        model.fit(X_train, y_train)
        pred = model.predict(X_test)[0]
        predictions.append(pred)
        actuals.append(y_test[0])

    mae = mean_absolute_error(actuals, predictions)

    model.fit(X_scaled, y)

    print("=== Model: Ridge Regression (Leave-One-Out CV) ===")
    print(f"Training pairs:       {len(pairs)}")
    print(f"Mean Absolute Error:  {mae:.1f} mg/dL")
    print(f"\nFeature coefficients (scaled):")
    for name, coef in zip(["lantus_units", "prev_waking_glucose"], model.coef_):
        print(f"  {name}: {coef:+.3f}")

    return model, scaler


def predict_tomorrow(model, scaler, lantus_tonight, waking_glucose_today):
    X_input = np.array([[lantus_tonight, waking_glucose_today]])
    X_scaled = scaler.transform(X_input)
    prediction = model.predict(X_scaled)[0]

    print(f"\n=== Tomorrow's Waking Glucose Prediction ===")
    print(f"Input — Lantus tonight:       {lantus_tonight} units")
    print(f"Input — Waking glucose today: {waking_glucose_today} mg/dL")
    print(f"Predicted waking glucose:     {prediction:.1f} mg/dL")
    print(f"\nNote: MAE tells you the typical error margin of this prediction.")
    print(f"Treat this as a directional estimate, not a clinical measurement.")

    return prediction


def run_model(df):
    pairs = build_waking_pairs(df)
    print(f"Built {len(pairs)} training pairs from waking + lantus data\n")

    model, scaler = train_and_evaluate(pairs)

    predict_tomorrow(
        model=model,
        scaler=scaler,
        lantus_tonight=18,
        waking_glucose_today=183
    )