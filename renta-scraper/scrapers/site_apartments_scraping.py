from typing import List, Optional
from bs4 import BeautifulSoup
import pandas as pd
from requests.exceptions import RequestException
from src.config import APARTMENTS_LINK, apartment_features
from src.utils import get_html_content


def extract_apartment_data(soup: BeautifulSoup, link: str) -> pd.DataFrame:
    """
    Extract data for an apartment from the BeautifulSoup object and return it as a DataFrame.

    Parameters:
        soup (BeautifulSoup): The BeautifulSoup object to extract data from.
        link (str): The source URL of the apartment data.

    Returns:
        DataFrame: A pandas DataFrame containing the extracted data.
    """
    apartment_data = {'source': link, 'sitename': 'apartments.com', 'image_source': '-1'}

    # Initialize all features to default value '-1'
    for feature in apartment_features:
        apartment_data[feature] = '-1'

    # Extract the required fields from the page
    # The implementation is straightforward, simply replace this comment
    # with the specific extraction logic provided.
    # ...

    # Compile amenities list and remove duplicates
    # ...

    # Append property images if available
    # ...

    # Return the apartment data as a pandas DataFrame
    return pd.DataFrame([apartment_data])


def get_apartments_links(initial_content: str) -> List[str]:
    """
    Extract the apartment links from the initial page content.

    Parameters:
        initial_content (str): The HTML content of the initial page.

    Returns:
        List[str]: A list of extracted apartment links.
    """
    article_links = []
    soup = BeautifulSoup(initial_content, "lxml")

    def extract_links(soup_obj: BeautifulSoup) -> None:
        placard_container = soup_obj.find("div", class_="placardContainer")
        if placard_container:
            posts = placard_container.find_all("li", class_="mortar-wrapper")
            for article in posts:
                data_url = article.find("article").get("data-url")
                article_links.append(data_url)

    extract_links(soup)

    # Extract pagination and additional pages if available
    # ...

    return article_links


def scrape_each_apartment_details(link: str) -> Optional[pd.DataFrame]:
    """
    Scrape the details of an apartment given a link.

    Parameters:
        link (str): The URL of the apartment to scrape.

    Returns:
        Optional[DataFrame]: A DataFrame with the apartment details or None if an error occurs.
    """
    try:
        content = get_html_content(link)
        article_soup = BeautifulSoup(content, "lxml")
        return extract_apartment_data(article_soup, link)
    except RequestException as e:
        print(f"Request error while scraping {link}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error while scraping {link}: {e}")
        return None


def main() -> pd.DataFrame:
    """
    Scrape apartment data from the APARTMENTS_LINK and compile the results into a DataFrame.

    Returns:
        DataFrame: A DataFrame containing all scraped apartment data.
    """
    all_apartments_df = pd.DataFrame()
    try:
        content = get_html_content(APARTMENTS_LINK)
    except RequestException as e:
        print(f"Request error while fetching the initial content: {e}")
        return all_apartments_df

    links = get_apartments_links(content)

    for link in links:
        apartment_data = scrape_each_apartment_details(link)
        if apartment_data is not None:
            all_apartments_df = pd.concat([all_apartments_df, apartment_data], ignore_index=True)

    return all_apartments_df


if __name__ == "__main__":
    df = main()
    # Optionally, you can save the DataFrame to a CSV file or handle it otherwise.
