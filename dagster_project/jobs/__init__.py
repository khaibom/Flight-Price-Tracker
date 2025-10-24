from dagster import define_asset_job

selection = ['extract_flight_offers', 'transform_flight_offers', 'load_flight_offers']
job_daily = define_asset_job(
    name="daily_flight_offers_job",
    selection=selection,
)