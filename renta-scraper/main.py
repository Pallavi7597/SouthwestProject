from scrapers import site_apartments_scraping
import pandas as pd

def scrape() -> None:
    """
    Execute the scraping function from the site_apartments_scraping module and save the results.

    The scraped data is saved to a CSV file named 'dataset.csv'.
    The row indices are not included in the CSV file to ensure only data is exported.
    """
    df = site_apartments_scraping.main()  # The main scraping function for apartments
    df.to_csv('dataset.csv', index=False)  # Export the DataFrame to a CSV file without row indices

if __name__ == "__main__":
    scrape()  # Initiate the scraping process when the script is executed directly
