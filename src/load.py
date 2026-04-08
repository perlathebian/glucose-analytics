import pandas as pd

def load_data(path="data/readings.csv"):
    df = pd.read_csv(path)
    
    df["timestamp"] = pd.to_datetime(df["date"] + " " + df["time"])
    df = df.drop(columns=["date", "time"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    
    df["hour"] = df["timestamp"].dt.hour
    df["day"] = df["timestamp"].dt.date
    
    return df

def summarize(df):
    print(f"Total readings:     {len(df)}")
    print(f"Date range:         {df['timestamp'].min()} → {df['timestamp'].max()}")
    print(f"Glucose min/max:    {df['glucose_mg_dl'].min()} / {df['glucose_mg_dl'].max()}")
    print(f"Glucose mean:       {df['glucose_mg_dl'].mean():.1f}")
    print(f"Missing glucose:    {df['glucose_mg_dl'].isna().sum()}")
    print(f"Waking readings:    {df['waking_reading'].sum()}")
    print(f"\nColumns:\n{df.dtypes}")