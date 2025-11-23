from dagster import Definitions, load_assets_from_modules

from .assets import flight_ticket, candlestick_chart
from .jobs import job_etl_daily, job_visualization_daily
from .schedules import schedule_daily_0900, schedule_daily_0930

all_assets = load_assets_from_modules([flight_ticket, candlestick_chart])
all_jobs = [job_etl_daily, job_visualization_daily]
all_schedules = [schedule_daily_0900, schedule_daily_0930]


defs = Definitions(
    assets=all_assets,
    jobs=all_jobs,
    schedules=all_schedules,
)