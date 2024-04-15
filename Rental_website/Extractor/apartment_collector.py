import requests
from bs4 import BeautifulSoup
import pandas as pd

from src.config import APARTMENTS_LINK, CHROME_DRIVER_PATH, column_order
from src.utils import fetch_website_html, reorder_dataframe_columns, format_current_date

def fetch_apartment_links():
    response = requests.get(APARTMENTS_LINK)
    soup = BeautifulSoup(response.text, 'html.parser')
    listings = soup.find_all('a', class_='placardTitle js-placardTitle ')
    return [listing['href'] for listing in listings]

def scrape_apartment_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    property_details = {
        "listing_title": soup.find('h1', class_='propertyName').text.strip(),
        "monthly_rental_price": soup.find('div', class_='rentInfoDetail').text.strip(),
        "address": soup.find('div', class_='propertyAddress').text.strip(),
        "latitude": None,  # This will need to be filled by geocoding the address if necessary
        "longitude": None,  # This will need to be filled by geocoding the address if necessary
        "property_management_name": soup.find('div', class_='managementCompany').text.strip() if soup.find('div', class_='managementCompany') else None,
        "unit_size": soup.find('div', class_='sqft').text.strip() if soup.find('div', class_='sqft') else None,
        "number_of_bedrooms": soup.find('div', class_='beds').text.strip() if soup.find('div', class_='beds') else None,
        "number_of_bathrooms": soup.find('div', class_='baths').text.strip() if soup.find('div', class_='baths') else None,
        "description": soup.find('section', class_='descriptionSection').text.strip(),
        "amenities_list": [amenity.text.strip() for amenity in soup.find_all('div', class_='amenity')],
        "property_type": "Apartment",  # Assuming all listings are apartments; adjust as needed
        "property_image_url": soup.find('img', class_='propertyImage')['src'] if soup.find('img', class_='propertyImage') else None,
        "lease_duration": soup.find('div', class_='leaseDuration').text.strip() if soup.find('div', class_='leaseDuration') else None
    }
    return property_details

def main():
    links = fetch_apartment_links()
    properties_list = []
    for link in links:
        property_data = scrape_apartment_data(link)
        properties_list.append(property_data)
    properties_df = pd.DataFrame(properties_list)
    properties_df = reorder_dataframe_columns(properties_df, column_order)
    print(properties_df)

if __name__ == "__main__":
    main()

