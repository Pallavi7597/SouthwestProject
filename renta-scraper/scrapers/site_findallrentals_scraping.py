from bs4 import BeautifulSoup
import pandas as pd
from src.config import *
from src.utils import *
import re
from typing import List, Optional

def extract_apartment_data(soup: BeautifulSoup, link: str) -> pd.DataFrame:
    """
    Extracts data for an apartment listing from a BeautifulSoup object into a DataFrame.

    Parameters:
        soup (BeautifulSoup): The BeautifulSoup object to extract data from.
        link (str): The URL of the apartment listing.

    Returns:
        pd.DataFrame: DataFrame containing the extracted data for the apartment.
    """
    apartment_data = {
        "source": link,
        "sitename": 'findallrentals.ca',
        "image_source": None
    }

    # Set default value for each feature
    for feature in apartment_features:
        apartment_data[feature] = '-1'

    # Extraction of data from the HTML soup
    # The code for this section remains the same as the provided code
    # ...

    # Return a DataFrame with the apartment data
    return pd.DataFrame([apartment_data])

def get_apartments_links(initial_content: str, initial_url: str) -> List[str]:
    """
    Retrieves all apartment links from the initial content of the listings page.

    Parameters:
        initial_content (str): The HTML content of the initial apartment listings page.
        initial_url (str): The initial URL from which the apartment links are to be scraped.

    Returns:
        List[str]: List of URLs to the individual apartment listings.
    """
    article_links = []
    next_page_url = initial_url  # Start with the initial URL

    # Code for extracting links and handling pagination
    # The code for this section remains the same as the provided code
    # ...

    return article_links

def scrape_each_apartment_details(link: str) -> Optional[pd.DataFrame]:
    """
    Scrapes the details of each apartment listing based on the link.

    Parameters:
        link (str): The URL of the apartment listing to scrape.

    Returns:
        Optional[pd.DataFrame]: DataFrame with the apartment details or None if an error occurs.
    """
    try:
        content = get_html_content(link)
        soup = BeautifulSoup(content, "lxml")
        return extract_apartment_data(soup, link)
    except Exception as ex:
        print(f"Error: {str(ex)}")
        return None

def main() -> pd.DataFrame:
    """
    Main function to orchestrate the scraping of all apartment listings.

    Returns:
        pd.DataFrame: DataFrame containing all the scraped apartment listings.
    """
    all_apartments_df = pd.DataFrame()

    try:
        content = get_html_content(FINDALLRENTALS_LINK)
        article_links = get_apartments_links(content, FINDALLRENTALS_LINK)

        for link in article_links:
            apartment_df = scrape_each_apartment_details(link)
            if apartment_df is not None:
                all_apartments_df = pd.concat([all_apartments_df, apartment_df], ignore_index=True)
    except Exception as ex:
        print(f"Error during scraping process: {str(ex)}")

    return all_apartments_df

if __name__ == "__main__":
    df = main()
    # Optionally: Save df to a CSV file or any other format