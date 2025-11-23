import pandas
from dagster import asset, RetryPolicy, Shape, Field
from Secret import API_SECRET, API_KEY
from amadeus import Client
from datetime import datetime, timedelta
from .parallel_search import flight_offers_bulk_search

departure_location = ["FRA", "DUS"]
return_location = ["HAN"]
departure_start = datetime.strptime("2026-02-15", "%Y-%m-%d")
departure_end = departure_start + timedelta(days=4)
return_start = datetime.strptime("2026-03-10", "%Y-%m-%d")
return_end = return_start + timedelta(days=11)

config_schema = Shape({
    'departure_start_date': Field(str, default_value=departure_start.strftime("%Y-%m-%d"), description='in "YYYY-MM-DD"'),
    'departure_end_date': Field(str, default_value=departure_end.strftime("%Y-%m-%d"), description='in "YYYY-MM-DD"'),
    'return_start_date': Field(str, default_value=return_start.strftime("%Y-%m-%d"), description='in "YYYY-MM-DD"'),
    'return_end_date': Field(str, default_value=return_end.strftime("%Y-%m-%d"), description='in "YYYY-MM-DD"'),
    'location_departure': Field(list, default_value=departure_location, description='location_departure'),
    'location_return': Field(list, default_value=return_location, description='location_return'),
})

@asset(
    name="extract_flight_offers",
    group_name="flights",
    compute_kind="python",
    retry_policy=RetryPolicy(max_retries=1, delay=10.0),
    config_schema=config_schema,
)
def extract_flight_offers(context) -> pandas.DataFrame:
    config = context.op_config
    departure_start_date = datetime.strptime(config.get("departure_start_date", str(departure_start)), "%Y-%m-%d")
    departure_end_date = datetime.strptime(config.get("departure_end_date", str(departure_end)), "%Y-%m-%d")
    return_start_date = datetime.strptime(config.get("return_start_date", str(return_start)), "%Y-%m-%d")
    return_end_date = datetime.strptime(config.get("return_end_date", str(return_end)), "%Y-%m-%d")
    dep_location = config.get("location_departure")
    ret_location = config.get("location_return")
    departure_range = [(departure_start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range((departure_end_date - departure_start_date).days + 1)]
    return_range = [(return_start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range((return_end_date - return_start_date).days + 1)]
    context.log.info(f"using departure range: {departure_range} \nreturn range: {return_range}")
    context.log.info(f"using departure location: {departure_location} \nreturn location: {ret_location}")


    amd_search_client = Client(
        client_id=API_KEY,
        client_secret=API_SECRET,
    )
    df = flight_offers_bulk_search(
        context,
        amd_search_client,
        dep_location,
        ret_location,
        departure_range,
        return_range,
        max_workers=10,
    )
    return df

@asset(
    name="transform_flight_offers",
    group_name="flights",
    compute_kind="python",
    retry_policy=RetryPolicy(max_retries=1, delay=10.0),
)
def transform_flight_offers(extract_flight_offers) -> pandas.DataFrame:
    return extract_flight_offers

@asset(
    name="load_flight_offers",
    group_name="flights",
    compute_kind="python",
    retry_policy=RetryPolicy(max_retries=1, delay=10.0),
)
def load_flight_offers(context, transform_flight_offers):
    df = transform_flight_offers
    df.to_csv("flight_prices.csv", mode="a", index=False, header=False)
    context.log.info("Data saved to flight_prices.csv")
    context.log.info(f'The min. price of df is: {df["price"].min()}')
    context.log.info(df.head())
