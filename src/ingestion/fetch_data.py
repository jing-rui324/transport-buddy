import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

LTA_ACCOUNT_KEY = os.getenv("LTA_ACCONT_KEY")
BASE_URL = "https://datamall2.mytransport.sg/ltaodataservice"

def fetch_lta_dataset(endpoint: str) -> dict:
    if not LTA_ACCOUNT_KEY:
        raise ValueError("LTA_ACCOUNT_KEY is not set in the environment variables.")
    
    headers = {
        "AccountKey": LTA_ACCOUNT_KEY,
        "accept": "application/json"
    }

    url = f"{BASE_URL}/{endpoint}"

    all_records = []
    skip_count = 0

    while True:
        params = {"$skip": skip_count}
        response = requests.get(url, headers=headers, params=params)
        
        data = response.json()
        batch = data.get("value", [])
        if not batch:
            break

        all_records.extend(batch)
        skip_count += 500 # API only returns 500 records per page
        
    return {"value": all_records}

def save_raw_data(data: dict, dataset_name: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{dataset_name}_{timestamp}.json"
    filepath = os.path.join("data/raw", filename)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Raw data saved to {filepath}")
    return filepath

if __name__ == "__main__":
    try:
        print("Fetching Bus Stops dataset...")
        raw_payload = fetch_lta_dataset("BusStops")
        save_raw_data(raw_payload, "bus_stops")
    except Exception as e:
        print(f"Error fetching Bus Stops dataset: {e}")