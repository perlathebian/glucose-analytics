import pandas as pd
from scipy import stats


def waking_glucose_stats(df):
    waking = df[df["waking_reading"] == 1].copy()

    print("=== Waking Glucose Stats ===")
    print(f"Count:        {len(waking)}")
    print(f"Mean:         {waking['glucose_mg_dl'].mean():.1f} mg/dL")
    print(f"Median:       {waking['glucose_mg_dl'].median():.1f} mg/dL")
    print(f"Std dev:      {waking['glucose_mg_dl'].std():.1f} mg/dL")
    print(f"Min:          {waking['glucose_mg_dl'].min():.1f} mg/dL")
    print(f"Max:          {waking['glucose_mg_dl'].max():.1f} mg/dL")
    print(f"Above 180:    {(waking['glucose_mg_dl'] > 180).sum()} / {len(waking)} days")
    print(f"Above 130:    {(waking['glucose_mg_dl'] > 130).sum()} / {len(waking)} days")
    print(f"In range:     {((waking['glucose_mg_dl'] >= 70) & (waking['glucose_mg_dl'] <= 130)).sum()} / {len(waking)} days")

    return waking


def lantus_vs_waking(df):
    df = df.copy().sort_values("timestamp").reset_index(drop=True)

    lantus_rows = df[df["lantus_units"] > 0][["timestamp", "lantus_units"]].copy()
    waking_rows = df[df["waking_reading"] == 1][["timestamp", "glucose_mg_dl"]].copy()

    pairs = []
    for _, lrow in lantus_rows.iterrows():
        future_waking = waking_rows[waking_rows["timestamp"] > lrow["timestamp"]]
        if not future_waking.empty:
            next_waking = future_waking.iloc[0]
            pairs.append({
                "lantus_units": lrow["lantus_units"],
                "lantus_time": lrow["timestamp"],
                "next_waking_glucose": next_waking["glucose_mg_dl"],
                "next_waking_time": next_waking["timestamp"],
            })

    result = pd.DataFrame(pairs)

    print("\n=== Lantus Dose vs Next Waking Glucose ===")
    print(result[["lantus_units", "next_waking_glucose"]].to_string(index=False))

    if len(result) >= 3:
        r, p = stats.pearsonr(result["lantus_units"], result["next_waking_glucose"])
        print(f"\nPearson correlation:  r = {r:.3f},  p = {p:.4f}")
        if p < 0.05:
            print("Statistically significant correlation.")
        else:
            print("No statistically significant correlation (expected with small dataset).")

    return result


def meal_spike_analysis(df):
    df = df.copy().sort_values("timestamp").reset_index(drop=True)

    df["next_glucose"] = df["glucose_mg_dl"].shift(-1)
    df["glucose_change"] = df["next_glucose"] - df["glucose_mg_dl"]

    pre_meal = df[df["meal_context"].isin(["pre_breakfast", "pre_lunch", "pre_dinner"])]
    pre_meal = pre_meal[pre_meal["glucose_change"].notna()].copy()

    print("\n=== Glucose Change After Each Meal Context ===")
    summary = pre_meal.groupby("meal_context")["glucose_change"].agg(
        count="count",
        mean="mean",
        std="std",
        min="min",
        max="max"
    ).round(1)
    print(summary.to_string())

    return pre_meal


def novorapid_effectiveness(df):
    df = df.copy().sort_values("timestamp").reset_index(drop=True)

    df["next_glucose"] = df["glucose_mg_dl"].shift(-1)
    df["glucose_change"] = df["next_glucose"] - df["glucose_mg_dl"]

    novo = df[(df["novorapid_units"] > 0) & (df["glucose_change"].notna())].copy()

    lowered = (novo["glucose_change"] < 0).sum()
    raised = (novo["glucose_change"] >= 0).sum()

    print("\n=== Novorapid Effectiveness ===")
    print(f"Total injections analyzed:  {len(novo)}")
    print(f"Glucose lowered after:      {lowered} ({lowered/len(novo)*100:.1f}%)")
    print(f"Glucose still rose after:   {raised} ({raised/len(novo)*100:.1f}%)")
    print(f"\nMean glucose change per dose:")
    print(novo.groupby("novorapid_units")["glucose_change"].mean().round(1).to_string())

    return novo