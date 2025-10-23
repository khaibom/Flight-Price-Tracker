import pandas as pd
from amadeus import ResponseError
from datetime import datetime
from itertools import product
import concurrent.futures as cf
import time

MAX_NUMBER_RETRIES = 3

def _flight_offers_search_worker(
    ctx,
    search_client,
    departure_loc: str,
    arrival_loc: str,
    departure_date: datetime,
    return_date: datetime,
    max_retries: int = MAX_NUMBER_RETRIES,
) -> pd.DataFrame | None:
    try:
        resp = search_client.shopping.flight_offers_search.get(
            originLocationCode=departure_loc,
            destinationLocationCode=arrival_loc,
            departureDate=departure_date,
            returnDate=return_date,
            adults=1,
            max=3,
        )
        min_data = min(resp.data, key=lambda x: float(x["price"]["total"]))
        ctx.log.info(
            f"Found flight from {departure_loc} to {arrival_loc} "
            f"({departure_date} - {return_date}) "
            f"min price {min_data['price']['total']}"
        )
        return pd.DataFrame(
            [
                {
                    "price": float(min_data["price"]["total"]),
                    "depart_date": departure_date,
                    "return_date": return_date,
                    "depart_location": departure_loc,
                    "arrival_location": arrival_loc,
                    "scrape_datetime": datetime.now().replace(microsecond=0),
                }
            ]
        )
    except ResponseError as e:
        ctx.log.warning(f"search failed for {departure_loc}->{arrival_loc} on {departure_date} - {return_date}: {e}")
        if max_retries > 0:
            # congestion control
            time.sleep(2 ** MAX_NUMBER_RETRIES - max_retries)
            ctx.log.info(f"retrying... {departure_loc}->{arrival_loc} on {departure_loc}->{arrival_loc} on {departure_date} - {return_date}: {max_retries} attempts left")
            return _flight_offers_search_worker(
                ctx,
                search_client,
                departure_loc,
                arrival_loc,
                departure_date,
                return_date,
                max_retries - 1,
            )
        else:
            ctx.log.warning(f"No results for {departure_loc}->{arrival_loc} on {departure_date} - {return_date}: {e}")
            return None

def flight_offers_bulk_search(
    ctx,
    search_client,
    departure_locations: list[str],
    return_locations: list[str],
    departure_range: list[datetime],
    return_range: list[datetime],
    max_workers: int = 7,
) -> pd.DataFrame:
    worker_params = product(departure_locations, return_locations, departure_range, return_range)
    frames: list[pd.DataFrame] = []
    with cf.ThreadPoolExecutor(max_workers=max_workers) as exe:
        for df in exe.map(lambda args: _flight_offers_search_worker(ctx, search_client, *args), worker_params):
            if df is not None and not df.empty:
                frames.append(df)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()