from Secret import API_SECRET, API_KEY
from amadeus import Client, ResponseError
import pandas as pd
import time
from datetime import datetime

GERMANY = ["FRA", "DUS"]
VIETNAM = ["HAN"]
DEPARTURE_RANGE = [f"2026-02-{15+x}" for x in range(5)] #start 15/02/2026 - 19/02/2026
RETURN_RANGE = [f"2026-03-{10+x}" for x in range(12)] #end 10/03/2026 - 11/03/2026

amadeus = Client(
    client_id=API_KEY,
    client_secret=API_SECRET,
)

columns = ["price", "depart", "return", "germany", "today"]
df = pd.DataFrame(columns=columns)
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
                        "depart": des,
                        "return": ret,
                        "germany": ger,
                        "today": datetime.today().strftime("%Y-%m-%d"),
                    }])
                ], ignore_index=True)

except ResponseError as error:
    print(error)
    raise error

df.to_csv("flight_prices.csv", mode="a", index=False, header=False) # pls just run 1 time per day
print(df["price"].min())
print(f"min price: {df.loc[df["price"].idxmin()]}")
print(df.head())