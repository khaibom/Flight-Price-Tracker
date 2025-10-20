import pandas as pd
import plotly.graph_objects as go

# Load CSV
cols = ["price", "depart_date", "return_date", "depart_location", "scrape_datetime"]
df = pd.read_csv("../../flight_prices.csv", names=cols, parse_dates=["depart_date", "return_date", "scrape_datetime"])

# Create a scrape date column (date only)
df["scrape_date"] = df["scrape_datetime"].dt.date

# Group by depart_date, return_date, depart_location, scrape_date
def ohlc_group(group):
    return pd.Series({
        "open": group.sort_values("scrape_datetime")["price"].iloc[0],
        "close": group.sort_values("scrape_datetime")["price"].iloc[-1],
        "high": group["price"].max(),
        "low": group["price"].min()
    })

ohlc = df.groupby(["depart_date","return_date","depart_location","scrape_date"]).apply(ohlc_group).reset_index()

# Example: plot candlestick for one combination
depart_date = "2026-02-16"
return_date = "2026-03-16"
depart_location = "DUS"
example = ohlc[(ohlc["depart_date"]==depart_date) & (ohlc["return_date"]==return_date) & (ohlc["depart_location"]==depart_location)]

fig = go.Figure(data=[go.Candlestick(
    x=example["scrape_date"],
    open=example["open"],
    high=example["high"],
    low=example["low"],
    close=example["close"],
    increasing_line_color="green",
    decreasing_line_color="red"
)])

fig.update_layout(
    title=f"Flight Prices Candlestick {depart_date} - {return_date}, {depart_location}",
    xaxis_title="Scrape Date",
    yaxis_title="Price (€)"
)

fig.show()
