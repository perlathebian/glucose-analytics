from src.load import load_data, summarize
from src.visualize import (
    plot_glucose_timeline,
    plot_hourly_distribution,
    plot_daily_average,
    plot_insulin_response
)

df = load_data()
summarize(df)

plot_glucose_timeline(df)
plot_hourly_distribution(df)
plot_daily_average(df)
plot_insulin_response(df)