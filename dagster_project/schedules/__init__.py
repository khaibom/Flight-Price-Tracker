from dagster import ScheduleDefinition, DefaultScheduleStatus

from ..jobs import (job_daily)

schedule_daily = ScheduleDefinition(
    job=job_daily,
    cron_schedule='0 9 * * *',
    execution_timezone='Europe/Berlin',
    default_status=DefaultScheduleStatus.RUNNING,
)