import requests
from datetime import datetime
import pandas as pd

def get_html_content(site: str) -> str:
    """
    Fetches and returns the HTML content from a specified website.

    Parameters:
        site (str): The URL of the website to fetch content from.

    Returns:
        str: The HTML content of the website.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    response = requests.get(site, headers=headers)
    response.raise_for_status()  # This will raise an exception for HTTP errors
    return response.text

def reorder_dataframe_columns(df: pd.DataFrame, column_order: list) -> pd.DataFrame:
    """
    Reorders the columns of a DataFrame based on a specified order, if they exist in the DataFrame.

    Parameters:
        df (pd.DataFrame): The DataFrame whose columns are to be reordered.
        column_order (list): A list of column names in the desired order.

    Returns:
        pd.DataFrame: The DataFrame with columns reordered.
    """
    # Filter the column_order to include only columns that exist in df
    filtered_column_order = [col for col in column_order if col in df.columns]
    return df[filtered_column_order]

def get_today_date_formatted() -> str:
    """
    Returns the current date formatted as 'YYYY-MM-DD'.

    Returns:
        str: The current date formatted as 'YYYY-MM-DD'.
    """
    return datetime.now().strftime('%Y-%m-%d')
