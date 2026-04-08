from src.load import load_data, summarize

df = load_data()
summarize(df)
print("\nFirst 5 rows:")
print(df.head())