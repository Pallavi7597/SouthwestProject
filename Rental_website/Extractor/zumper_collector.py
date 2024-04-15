import requests
from bs4 import BeautifulSoup
import pandas as pd

from src.config import ZUMPER_LINK, column_order
from src.utils import fetch_website_html, reorder_dataframe_columns, format_current_date

def fetch_zumper_links():
    response = requests.get(ZUMPER_LINK)
    soup = BeautifulSoup(response.text, 'html.parser')
    listings = soup.find_all('a', class_='listing-result')
    return [listing['href'] for listing in listings]

def scrape_zumper_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    property_details = {
        "listing_title": soup.find('h1', class_='listing-name').text.strip(),
        "monthly_rental_price": soup.find('span', class_='price').text.strip(),
        "description": soup.find('div', class_='description').text.strip(),
        "amenities_list": [feature.text for feature in soup.find_all('div', class_='amenity-feature')],
        "address": soup.find('div', class_='address').text.strip() if soup.find('div', class_='address') else None,
        "latitude": None,  # This will need to be filled by geocoding the address if necessary
        "longitude": None,  # This will need to be filled by geocoding the address if necessary
        "property_management_name": soup.find('div', class_='management').text.strip() if soup.find('div', class_='management') else None,
        "unit_size": soup.find('div', class_='unit-size').text.strip() if soup.find('div', class_='unit-size') else None,
        "number_of_bedrooms": soup.find('div', class_='bedrooms').text.strip() if soup.find('div', class_='bedrooms') else None,
        "number_of_bathrooms": soup.find('div', class_='bathrooms').text.strip() if soup.find('div', class_='bathrooms') else None,
        "property_type": "Apartment",  # Assuming all listings on Zumper are apartments; adjust as needed
        "property_image_url": soup.find('img', class_='property-image')['src'] if soup.find('img', class_='property-image') else None,
        "lease_duration": soup.find('div', class_='lease-duration').text.strip() if soup.find('div', class_='lease-duration') else None,
    }
    return property_details

def main():
    links = fetch_zumper_links()
    properties_list = []
    for link in links:
        property_data = scrape_zumper_data(link)
        properties_list.append(property_data)
    properties_df = pd.DataFrame(properties_list)
    properties_df = reorder_dataframe_columns(properties_df, column_order)
    print(properties_df)

if __name__ == "__main__":
    main()


