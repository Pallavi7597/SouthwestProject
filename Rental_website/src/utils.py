import requests
from datetime import datetime
import pandas as pd

def fetch_website_html(url: str) -> str:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raises an exception for HTTP errors
    return response.text

def reorder_dataframe_columns(dataframe: pd.DataFrame, desired_order: list) -> pd.DataFrame:
    valid_columns = [column for column in desired_order if column in dataframe.columns]
    return dataframe[valid_columns]

def format_current_date() -> str:
    return datetime.now().strftime('%Y-%m-%d')
