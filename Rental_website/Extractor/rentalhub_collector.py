import requests
from bs4 import BeautifulSoup
import pandas as pd

from src.config import FINDALLRENTALS_LINK, column_order
from src.utils import fetch_website_html, reorder_dataframe_columns, format_current_date

def fetch_rentalhub_links():
    response = requests.get(FINDALLRENTALS_LINK)
    soup = BeautifulSoup(response.text, 'html.parser')
    listings = soup.find_all('a', class_='listing-card')
    return [listing['href'] for listing in listings]

def scrape_rentalhub_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    property_details = {
       "listing_title": soup.find('h1', class_='listing-title').text.strip(),  # Adjust class names as needed
        "monthly_rental_price": soup.find('span', class_='price').text.strip(),
        "address": soup.find('span', class_='address').text.strip(),
        "latitude": None,  # This will need to be filled by geocoding the address if necessary
        "longitude": None,  # This will need to be filled by geocoding the address if necessary
        "property_management_name": soup.find('span', class_='management-company').text.strip() if soup.find('span', class_='management-company') else None,
        "unit_size": soup.find('span', class_='size').text.strip() if soup.find('span', class_='size') else None,
        "number_of_bedrooms": soup.find('span', class_='bedrooms').text.strip() if soup.find('span', class_='bedrooms') else None,
        "number_of_bathrooms": soup.find('span', class_='bathrooms').text.strip() if soup.find('span', class_='bathrooms') else None,
        "description": soup.find('div', class_='description').text.strip(),
        "amenities_list": [amenity.text.strip() for amenity in soup.find_all('li', class_='amenity')],
        "property_type": "Apartment",  # Assuming all listings are apartments; adjust as needed
        "property_image_url": soup.find('img', class_='property-image')['src'] if soup.find('img', class_='property-image') else None,
        "lease_duration": soup.find('div', class_='lease-info').text.strip() if soup.find('div', class_='lease-info') else None
    }
    return property_details

def main():
    links = fetch_rentalhub_links()
    properties_list = []
    for link in links:
        property_data = scrape_rentalhub_data(link)
        properties_list.append(property_data)
    properties_df = pd.DataFrame(properties_list)
    properties_df = reorder_dataframe_columns(properties_df, column_order)
    print(properties_df)

if __name__ == "__main__":
    main()

