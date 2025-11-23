import re
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from dagster import Shape, Field, asset, RetryPolicy, MetadataValue, Output

departure_location = "DUS"
return_location = "HAN"
departure_time = datetime.strptime("2026-02-16", "%Y-%m-%d")
return_time = datetime.strptime("2026-03-16", "%Y-%m-%d")

viz_config_schema = Shape({
    'departure_date': Field(str, default_value=departure_time.strftime("%Y-%m-%d"), description='in "YYYY-MM-DD"'),
    'return_date': Field(str, default_value=return_time.strftime("%Y-%m-%d"), description='in "YYYY-MM-DD"'),
    'location_departure': Field(str, default_value=departure_location, description='location_departure'),
    'location_return': Field(str, default_value=return_location, description='location_return'),
})

@asset(
    name="candlestick_chart",
    group_name="visualization",
    compute_kind="python",
    retry_policy=RetryPolicy(max_retries=1, delay=10.0),
    config_schema=viz_config_schema,
    #deps=[AssetKey("load_flight_offers")],
)
def candlestick_chart(context):
    config = context.op_config
    dep_date_str = config.get("departure_date", departure_time.strftime("%Y-%m-%d"))
    ret_date_str = config.get("return_date", return_time.strftime("%Y-%m-%d"))
    dep_location = config.get("location_departure", departure_location)
    ret_location = config.get("location_return", return_location)
    dep_date = pd.to_datetime(dep_date_str).normalize()
    ret_date = pd.to_datetime(ret_date_str).normalize()

    CURRENT_DIR = Path(__file__).parent
    CSV_PATH = (CURRENT_DIR / "../../flight_prices.csv").resolve()
    cols = ["price", "depart_date", "return_date", "depart_location", "return_location", "scrape_datetime"]
    df = pd.read_csv(CSV_PATH, names=cols, header=None, parse_dates=["depart_date", "return_date", "scrape_datetime"])
    df["scrape_date"] = df["scrape_datetime"].dt.date
    df_sorted = df.sort_values("scrape_datetime")

    # Group by depart_date, return_date, depart_location, return_location, scrape_date
    ohlc = (
        df_sorted
        .groupby(
            ["depart_date", "return_date", "depart_location", "return_location", "scrape_date"],
            as_index=False
        )
        .agg(
            open=("price", "first"),
            close=("price", "last"),
            high=("price", "max"),
            low=("price", "min"),
        )
    )
    example = ohlc[(ohlc["depart_date"]==dep_date) &
                   (ohlc["return_date"]==ret_date) &
                   (ohlc["depart_location"]==dep_location) &
                   (ohlc["return_location"]==ret_location)]

    fig = go.Figure(data=[go.Candlestick(
        x=example["scrape_date"],
        open=example["open"],
        high=example["high"],
        low=example["low"],
        close=example["close"],
        increasing_line_color="red",
        decreasing_line_color="green"
    )])

    fig.update_layout(
        title=f"Flight Prices Candlestick {dep_date} - {ret_date}, {dep_location} <-> {ret_location}",
        xaxis_title="Scrape Date",
        yaxis_title="Price (€)"
    )

    title_for_fn = f"{dep_location}_{ret_location}_{dep_date_str}_{ret_date_str}"
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", title_for_fn)
    html_path = Path(f"flight_prices_{safe}.html")
    fig.write_html(str(html_path), include_plotlyjs="cdn")

    md_lines = [
        f"**Depart Location:** `{dep_location}` | **Return Location:** `{dep_location}` | **Depart:** `{dep_date}` | **Return:** `{ret_date}`",
        f"**Points:** {len(example)} scrape days",
        f"**Min/Max:** €{example['low'].min():.2f} / €{example['high'].max():.2f}",
    ]
    metadata = {
        "html": MetadataValue.path(html_path),
        "summary": MetadataValue.md("\n\n".join(md_lines)),
        "rows_used": len(example),
        "depart_date": MetadataValue.text(dep_date_str),
        "return_date": MetadataValue.text(ret_date_str),
        "depart_location": MetadataValue.text(dep_location),
        "return_location": MetadataValue.text(ret_location),
    }


    return Output(html_path, metadata=metadata)
