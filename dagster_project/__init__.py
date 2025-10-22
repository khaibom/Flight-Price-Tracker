from dagster import Definitions, load_assets_from_modules

from .assets import plane_tickets
from .jobs import job_daily
from .schedules import schedule_daily

all_assets = load_assets_from_modules([plane_tickets])
all_jobs = [job_daily]
all_schedules = [schedule_daily]


defs = Definitions(
    assets=all_assets,
    jobs=all_jobs,
    schedules=all_schedules,
)