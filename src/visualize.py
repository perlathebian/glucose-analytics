import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns


def plot_glucose_timeline(df):
    fig, ax = plt.subplots(figsize=(16, 6))

    ax.plot(df["timestamp"], df["glucose_mg_dl"],
            color="steelblue", linewidth=1.5, zorder=1)

    ax.scatter(df["timestamp"], df["glucose_mg_dl"],
               color="steelblue", s=40, zorder=2)

    novo = df[df["novorapid_units"] > 0]
    ax.scatter(novo["timestamp"], novo["glucose_mg_dl"],
               color="orange", s=80, zorder=3,
               label="Novorapid given", marker="v")

    lantus = df[df["lantus_units"] > 0]
    ax.scatter(lantus["timestamp"], lantus["glucose_mg_dl"],
               color="red", s=80, zorder=3,
               label="Lantus given", marker="^")

    waking = df[df["waking_reading"] == 1]
    ax.scatter(waking["timestamp"], waking["glucose_mg_dl"],
               color="green", s=100, zorder=4,
               label="Waking reading", marker="D")

    ax.axhline(y=180, color="red", linestyle="--",
               linewidth=1, label="High threshold (180)")
    ax.axhline(y=130, color="green", linestyle="--",
               linewidth=1, label="Target ceiling (130)")
    ax.axhline(y=70, color="purple", linestyle="--",
               linewidth=1, label="Low threshold (70)")

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax.xaxis.set_major_locator(mdates.DayLocator())
    plt.xticks(rotation=45)

    ax.set_title("Glucose Levels Over Time with Insulin Events", fontsize=14)
    ax.set_xlabel("Date")
    ax.set_ylabel("Glucose (mg/dL)")
    ax.legend(loc="upper right")

    plt.tight_layout()
    plt.savefig("outputs/glucose_timeline.png", dpi=150)
    plt.show()
    print("Saved: outputs/glucose_timeline.png")


def plot_hourly_distribution(df):
    fig, ax = plt.subplots(figsize=(12, 5))

    sns.boxplot(x="hour", y="glucose_mg_dl", data=df,
                color="lightblue", ax=ax)

    ax.axhline(y=180, color="red", linestyle="--", linewidth=1)
    ax.axhline(y=130, color="green", linestyle="--", linewidth=1)

    ax.set_title("Glucose Distribution by Hour of Day", fontsize=14)
    ax.set_xlabel("Hour of Day (24h)")
    ax.set_ylabel("Glucose (mg/dL)")

    plt.tight_layout()
    plt.savefig("outputs/hourly_distribution.png", dpi=150)
    plt.show()
    print("Saved: outputs/hourly_distribution.png")


def plot_daily_average(df):
    daily = df.groupby("day")["glucose_mg_dl"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.bar(daily["day"].astype(str), daily["glucose_mg_dl"],
           color="steelblue", alpha=0.7)

    ax.axhline(y=180, color="red", linestyle="--",
               linewidth=1, label="High threshold (180)")
    ax.axhline(y=130, color="green", linestyle="--",
               linewidth=1, label="Target ceiling (130)")

    ax.set_title("Average Daily Glucose", fontsize=14)
    ax.set_xlabel("Date")
    ax.set_ylabel("Average Glucose (mg/dL)")
    ax.legend()
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig("outputs/daily_average.png", dpi=150)
    plt.show()
    print("Saved: outputs/daily_average.png")


def plot_insulin_response(df):
    df = df.copy().sort_values("timestamp").reset_index(drop=True)
    df["next_glucose"] = df["glucose_mg_dl"].shift(-1)
    df["glucose_change"] = df["next_glucose"] - df["glucose_mg_dl"]

    novo = df[(df["novorapid_units"] > 0) & (df["glucose_change"].notna())]

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.scatter(novo["novorapid_units"], novo["glucose_change"],
               color="darkorange", s=80, zorder=2)

    for _, row in novo.iterrows():
        ax.annotate(f"{int(row['novorapid_units'])}u",
                    (row["novorapid_units"], row["glucose_change"]),
                    textcoords="offset points", xytext=(6, 4), fontsize=8)

    ax.axhline(0, color="black", linewidth=0.8)

    ax.set_title("Novorapid Dose vs Glucose Change to Next Reading", fontsize=13)
    ax.set_xlabel("Novorapid Dose (units)")
    ax.set_ylabel("Glucose Change to Next Reading (mg/dL)")

    plt.tight_layout()
    plt.savefig("outputs/insulin_response.png", dpi=150)
    plt.show()
    print("Saved: outputs/insulin_response.png")