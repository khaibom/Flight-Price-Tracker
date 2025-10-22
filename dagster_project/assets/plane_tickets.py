import pandas
from dagster import asset, RetryPolicy

from Secret import API_SECRET, API_KEY
from amadeus import Client, ResponseError
import pandas as pd
import time
from datetime import datetime

GERMANY = ["FRA", "DUS"]
VIETNAM = ["HAN"]
DEPARTURE_RANGE = [f"2026-02-{15+x}" for x in range(5)] #start 15/02/2026 - 19/02/2026
RETURN_RANGE = [f"2026-03-{10+x}" for x in range(12)] #return 10/03/2026 - 21/03/2026

@asset(
    name="extract_flight_offers",
    group_name="flights",
    compute_kind="python",
    retry_policy=RetryPolicy(max_retries=1, delay=10.0),
)
def extract_flight_offers(context) -> pandas.DataFrame:
    amadeus = Client(
        client_id=API_KEY,
        client_secret=API_SECRET,
    )
    cols = ["price", "depart_date", "return_date", "depart_location", "scrape_datetime"]
    df = pd.DataFrame(columns=cols)
    try:
        for ger in GERMANY:
            for des in DEPARTURE_RANGE:
                for ret in RETURN_RANGE:
                    time.sleep(0.2)
                    response = amadeus.shopping.flight_offers_search.get(
                        originLocationCode=ger,
                        destinationLocationCode="HAN",
                        departureDate=des,
                        returnDate=ret,
                        adults=1,
                        max=3
                    )
                    min_data = min(response.data, key=lambda x: float(x["price"]["total"]))
                    df = pd.concat([
                        df,
                        pd.DataFrame([{
                            "price": float(min_data["price"]["total"]),
                            "depart_date": des,
                            "return_date": ret,
                            "depart_location": ger,
                            "scrape_datetime": datetime.now().replace(microsecond=0),
                        }])
                    ], ignore_index=True)
                    context.log.info(f"Found flight from {ger} to 'HAN' {des} - {ret} with price {min_data['price']['total']}")
    except ResponseError as error:
        print(error)
        raise error
    return df


@asset(
    name="load_flight_offers",
    group_name="flights",
    compute_kind="python",
    retry_policy=RetryPolicy(max_retries=1, delay=10.0),
)
def load_flight_offers(context, extract_flight_offers):
    df = extract_flight_offers()
    df.to_csv("flight_prices.csv", mode="a", index=False, header=False)
    context.log.info("Data saved to flight_prices.csv")
    print(df["price"].min())
    print(f"min price: {df.loc[df['price'].idxmin()]}")
    print(df.head())
