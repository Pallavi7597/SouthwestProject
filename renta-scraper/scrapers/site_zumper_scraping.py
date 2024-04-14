from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

from src.config import CHROME_DRIVER_PATH, ZUMPER_LINK, apartment_features
from src.utils import get_today_date_formatted

def extract_amenities(html_content: str) -> str:
    """Extracts amenities from the given HTML content."""
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        amenities_section = soup.find("section", id="amenities")
        amenities = [cell.text.strip() for cell in amenities_section.find_all("td", class_="css-rtks1j") if cell.text.strip()] if amenities_section else []
        return ", ".join(amenities) if amenities else "-1"
    except Exception as e:
        print(f"Error extracting amenities: {e}")
        return "-1"

def extract_apartment_data(link: str, driver: webdriver.Chrome) -> pd.DataFrame:
    """Scrapes apartment data for the given link using the provided driver."""
    print(f"Scraping article: {link}")
    driver.get(link)
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    
    apartment_data = {key: '-1' for key in apartment_features}
    apartment_data.update({
        "source": link,
        "sitename": 'zumper.com',
        "building_name": soup.find("h1", class_="chakra-heading css-za1032-display32To40").text.strip(),
        "listing_name": soup.find("h1", class_="chakra-heading css-za1032-display32To40").text.strip(),
        "address": soup.find("address", class_="chakra-text").text.strip(),
        "amenities": extract_amenities(content),
        "property_image": soup.select_one('div.css-138u0vj picture img')['src'] if soup.select_one('div.css-138u0vj picture img') else '-1'
    })

    # Additional data extraction logic remains the same.
    # ...

    return pd.DataFrame([apartment_data])

def get_apartments_links(link: str, driver: webdriver.Chrome) -> list:
    """Fetches apartment listing links from the given page link using the provided driver."""
    driver.get(link)
    time.sleep(6)  # Wait for dynamic content to load.
    links = [element.get_attribute('href') for element in driver.find_elements(By.CSS_SELECTOR, ".css-8a605h .css-0 a")]
    return [link if link.startswith('http') else f"https://www.zumper.com{link}" for link in links]

def main() -> pd.DataFrame:
    """Orchestrates the scraping process of apartment listings."""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    
    with webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=options) as driver:
        all_apartments_df = pd.DataFrame()
        zumper_today_link = f"{ZUMPER_LINK}?available-before={get_today_date_formatted()}&min-active-units=1"
        links = get_apartments_links(zumper_today_link, driver)

        for link in links:
            try:
                apartment_df = extract_apartment_data(link, driver)
                all_apartments_df = pd.concat([all_apartments_df, apartment_df], ignore_index=True)
            except Exception as ex:
                print(f"Error scraping {link}: {str(ex)}")
    
    return all_apartments_df

if __name__ == "__main__":
    df = main()
