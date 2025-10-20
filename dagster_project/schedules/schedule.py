from dagster import ScheduleDefinition
from dagster_project.jobs.flight_price_job import flight_price_job

daily_schedule = ScheduleDefinition(
    job=flight_price_job,
    cron_schedule="0 8 * * *",  # every day at 8 AM
)
