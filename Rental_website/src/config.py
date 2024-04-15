# Configuration for web scraping
APARTMENTS_LINK = "https://www.apartments.com/apartments/halifax-ns/?bb=smmkxog_tO5n6q4x-4vF"
FINDALLRENTALS_LINK = "https://findallrentals.ca/for-rent?location=halifax-county&property_types=apartment"
ZUMPER_LINK = "https://www.zumper.com/apartments-for-rent/halifax-ns/"
ZILLOW_LINK = "https://www.zillow.com/halifax-ns/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-64.17517786914064%2C%22east%22%3A-63.09577113085938%2C%22south%22%3A44.371977832121544%2C%22north%22%3A44.919120866715815%7D%2C%22usersSearchTerm%22%3A%22Halifax%2C%20NS%22%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A791204%2C%22regionType%22%3A6%7D%5D%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%7D"
KIJIJI_LINK = "https://www.kijiji.ca/b-real-estate/city-of-halifax/c34l1700321"

# Configuration for web scraping
CHROME_DRIVER_PATH = "/home/surya/.wdm/drivers/chromedriver/linux64/111.0.5563.64/chromedriver"

# Column ordering for data presentation
column_order = [
    "sitename", "source", "listing_name", "building_name", "apartment_number",
    "address", "add_lat", "add_long", "property_management_name", "monthly_rent",
    "property_type", "bedroom_count", "bathroom_count", "apartment_size",
    "amenities", "property_image", "lease_period"
]
