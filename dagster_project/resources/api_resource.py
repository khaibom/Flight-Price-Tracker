from dagster import resource
from Secret import API_SECRET, API_KEY

@resource
def api_resource():
    return {
        "API_SECRET": API_SECRET,
        "API_KEY": API_KEY,
    }
