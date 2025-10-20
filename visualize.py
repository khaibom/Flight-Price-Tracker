import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
from matplotlib.animation import FuncAnimation

cols = ["price", "depart_date", "return_date", "depart_location", "scrape_datetime"]
df = pd.read_csv("flight_prices.csv", names=cols)

df["depart_date"] = pd.to_datetime(df["depart_date"])
df["return_date"] = pd.to_datetime(df["return_date"])
df["scrape_datetime"] = pd.to_datetime(df["scrape_datetime"])

def visual1(df):
    for (dep, ret), group in df.groupby(["depart_date", "return_date"]):
        plt.plot(group["scrape_datetime"], group["price"], marker="o", label=f"{dep} -> {ret}")
        plt.title(f"Price Change Over Time by {dep} -> {ret}")
        plt.xlabel("Scrape Date")
        plt.ylabel("Price")
        plt.legend(title=f"Price Change Over Time by {dep} -> {ret}")
        plt.tight_layout()
        plt.show()

def visual2(df):
    for dep, sub_df in df.groupby("depart_date"):
        plt.figure(figsize=(8, 4))
        for ret, group in sub_df.groupby("scrape_datetime"):
            plt.plot(group["scrape_datetime"], group["price"], marker="o", label=ret.strftime("%Y-%m-%d"))
        plt.title(f"Price evolution for departure {dep.strftime('%Y-%m-%d')}")
        plt.xlabel("Scrape Date")
        plt.ylabel("Price (€)")
        plt.legend(title="Return Date", fontsize=8)
        plt.tight_layout()
        plt.show()

def visual3(df):
    pivot = df.pivot_table(
        index="depart_date",
        columns="return_date",
        values="price",
        aggfunc="mean"
    )
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="coolwarm")
    plt.title("Average Flight Prices (Depart vs. Return)")
    plt.xlabel("Return Date")
    plt.ylabel("Departure Date")
    plt.show()

def visual4(df):
    for loc, group in df.groupby("depart_location"):
        plt.figure(figsize=(8, 4))
        for dep in group["depart_date"].unique():
            sub = group[group["depart_date"] == dep]
            plt.plot(sub["scrape_datetime"], sub["price"], label=f"Dep {dep.strftime('%m-%d')}")
        plt.title(f"Price Trend over Time ({loc})")
        plt.xlabel("Scrape Date")
        plt.ylabel("Price (€)")
        plt.legend(fontsize=8)
        plt.tight_layout()
        plt.show()

def visual5(df):
    # Keep only relevant scrape dates if many exist
    latest_scrape = df["scrape_datetime"].max()

    # Use Seaborn FacetGrid
    g = sns.FacetGrid(df, col="depart_location", hue="depart_date", height=4, aspect=1.3)
    g.map_dataframe(sns.lineplot, x="return_date", y="price")
    g.add_legend(title="Departure Date")

    g.set_axis_labels("Return Date", "Price (€)")
    g.set_titles(col_template="{col_name}")
    plt.suptitle(f"Flight Prices by Return Date and Departure (Scraped {latest_scrape.date()})", y=1.05)
    plt.tight_layout()
    plt.show()

def visual6(df):
    df["depart_ordinal"] = df["depart_date"].map(pd.Timestamp.toordinal)
    df["return_ordinal"] = df["return_date"].map(pd.Timestamp.toordinal)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")

    ax.scatter(df["depart_ordinal"], df["return_ordinal"], df["price"],
               c=df["price"], cmap="viridis", s=40)

    ax.set_xlabel("Departure Date")
    ax.set_ylabel("Return Date")
    ax.set_zlabel("Price (€)")

    # Pretty axis labels
    xticks = sorted(df["depart_ordinal"].unique())
    yticks = sorted(df["return_ordinal"].unique())
    ax.set_xticks(xticks)
    ax.set_xticklabels([pd.to_datetime(x).strftime("%m-%d") for x in xticks], rotation=45)
    ax.set_yticks(yticks)
    ax.set_yticklabels([pd.to_datetime(y).strftime("%m-%d") for y in yticks], rotation=45)

    plt.title("3D View of Flight Prices")
    plt.tight_layout()
    plt.show()

def visual7(df):
    df["depart_date_str"] = df["depart_date"].dt.strftime("%m-%d")
    df["return_date_str"] = df["return_date"].dt.strftime("%m-%d")

    scrape_datetimes = sorted(df["scrape_datetime"].unique())
    fig, ax = plt.subplots(figsize=(8, 6))

    def update(frame):
        ax.clear()
        sub = df[df["scrape_datetime"] == frame]
        pivot = sub.pivot_table(index="depart_date_str", columns="return_date_str", values="price", aggfunc="mean")
        sns.heatmap(pivot, cmap="coolwarm", ax=ax, cbar=True, vmin=df["price"].min(), vmax=df["price"].max())
        ax.set_title(f"Flight Prices — Scraped on {frame.date()}")
        plt.xlabel("Return Date")
        plt.ylabel("Departure Date")

    ani = FuncAnimation(fig, update, frames=scrape_datetimes, repeat=False)
    plt.show()

def visual8(df):
    df["scrape_datetime"] = df["scrape_datetime"].dt.date
    fig = px.scatter_3d(
        df,
        x="depart_date",
        y="return_date",
        z="price",
        color="depart_location",
        size="price",
        animation_frame="scrape_datetime",
        title="Flight Prices Over Time"
    )
    fig.update_layout(scene=dict(
        xaxis_title='Departure Date',
        yaxis_title='Return Date',
        zaxis_title='Price (€)'
    ))
    fig.show()

visual8(df)
