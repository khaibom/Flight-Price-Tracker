from dagster import ScheduleDefinition, DefaultScheduleStatus

from ..jobs import (job_etl_daily, job_visualization_daily)

schedule_daily_0900 = ScheduleDefinition(
    job=job_etl_daily,
    cron_schedule='0 9 * * *',
    execution_timezone='Europe/Berlin',
    default_status=DefaultScheduleStatus.RUNNING,
)

schedule_daily_0930 = ScheduleDefinition(
    job=job_visualization_daily,
    cron_schedule='30 9 * * *',
    execution_timezone='Europe/Berlin',
    default_status=DefaultScheduleStatus.RUNNING,
)