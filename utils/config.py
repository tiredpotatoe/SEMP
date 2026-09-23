import json
from pathlib import Path

current_dir = Path(__file__).resolve().parent
config_path = (current_dir / ".." / "config.json").resolve()

with open(config_path, "r") as file:
    config = json.load(file)

OPENLIBRARY_SEARCH_URL = config["openlibrary_search_url"]
SEARCH_QUERY = config["search_query"]
FIELDS = config["fields"]
FETCH_LIMIT = config["fetch_limit"]
YEAR_CUTOFF = config["year_cutoff"]
REQUEST_TIMEOUT = config["request_timeout"]
OUTPUT_CSV_PATH = Path(config["output_csv_path"])  