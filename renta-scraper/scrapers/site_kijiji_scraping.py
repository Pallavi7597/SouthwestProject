from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import re

from src.config import KIJIJI_LINK, apartment_features
from src.utils import get_html_content

def extract_apartment_size(soup: BeautifulSoup) -> str:
    """Extracts the apartment size from the provided soup object."""
    for li_tag in soup.find_all("li", class_="twoLinesAttribute-633292638"):
        if li_tag.find("dt", class_="twoLinesLabel-2332083105", text="Size (sqft)"):
            size_dd_tag = li_tag.find("dd", class_="twoLinesValue-2653438411")
            if size_dd_tag:
                return f"{size_dd_tag.get_text(strip=True).replace('\n', '')} sqft"
    return "-1"

def extract_amenities(html_content: str) -> str:
    """Extracts amenities from the provided HTML content."""
    soup = BeautifulSoup(html_content, "html.parser")
    amenities_container = soup.select_one("#vip-body > div.itemAttributeCarousel-3991134065 > div.gradientScrollWrapper-2207830989 > div > div > div:nth-child(3) > ul")
    if amenities_container:
        amenities = [li.text.strip() for li in amenities_container.select("li.groupItem-1182798569.available-1766233427")]
        return ", ".join(amenities) if amenities else "-1"
    return "-1"

def extract_apartment_data(article: str, html_content: str) -> pd.DataFrame:
    """Extracts all relevant apartment data from the provided HTML content and returns it as a DataFrame."""
    soup = BeautifulSoup(html_content, 'html.parser')
    listing_details = {feature: '-1' for feature in apartment_features}
    listing_details.update({
        "source": article,
        "sitename": 'Kijiji.ca',
        "property_management_name": soup.select_one("#vip-body > div.itemInfoSidebar-1618727533.itemInfoSidebar__newRentals-3969318677 > div:nth-child(4) > div > div.header-1351916284.headerWithAvatar-2912394077 > div > a").text.strip() if soup.select_one("#vip-body > div.itemInfoSidebar-1618727533.itemInfoSidebar__newRentals-3969318677 > div:nth-child(4) > div > div.header-1351916284.headerWithAvatar-2912394077 > div > a") else "-1",
        "bedroom_count": soup.select_one("#vip-body > div.realEstateTitle-389420867 > div.unitRow-2439405931 > div > li:nth-child(2) > span").text.strip().split(":")[-1].strip() if soup.select_one("#vip-body > div.realEstateTitle-389420867 > div.unitRow-2439405931 > div > li:nth-child(2) > span") else "-1",
        "bathroom_count": soup.select_one("#vip-body > div.realEstateTitle-389420867 > div.unitRow-2439405931 > div > li:nth-child(3) > span").text.strip().split(":")[-1].strip() if soup.select_one("#vip-body > div.realEstateTitle-389420867 > div.unitRow-2439405931 > div > li:nth-child(3) > span") else "-1",
        "amenities": extract_amenities(html_content),
        "lease_period": soup.select_one("#vip-body > div.itemAttributeCarousel-3991134065 > div.gradientScrollWrapper-2207830989 > div > div > div:nth-child(1) > ul > li:nth-child(4) > dl > dd").text.strip() if soup.select_one("#vip-body > div.itemAttributeCarousel-3991134065 > div.gradientScrollWrapper-2207830989 > div > div > div:nth-child(1) > ul > li:nth-child(4) > dl > dd") else "-1",
        "listing_name": soup.find("h1", class_="title-4206718449").text.strip() if soup.find("h1", class_="title-4206718449") else "-1",
        "address": soup.find("span", itemprop="address").text.strip() if soup.find("span", itemprop="address") else "-1",
        "monthly_rent": soup.find("div", class_="priceWrapper-3915768379").find("span").text.strip().split('.')[0] if soup.find("div", class_="priceWrapper-3915768379") and soup.find("div", class_="priceWrapper-3915768379").find("span") else "-1",
        "apartment_size": extract_apartment_size(soup),
        "property_image": soup.find("div", class_="thumbnailContainer-178432056").find("img")['src'] if soup.find("div", class_="thumbnailContainer-178432056") and soup.find("div", class_="thumbnailContainer-178432056").find("img") and 'src' in soup.find("div", class_="thumbnailContainer-178432056").find("img").attrs else "-1"
    })

    return pd.DataFrame([listing_details])

def get_apartments_links(initial_content: str, initial_url: str) -> list:
    """Extracts apartment listing URLs from the initial content and manages pagination."""
    article_links = []
    next_page_url = initial_url  # Start with the initial URL
    while next_page_url:
        soup = BeautifulSoup(initial_content, "lxml")
        for h3 in soup.find_all("h3", {"data-testid": "listing-title"}):
            a_tag = h3.find("a", {"data-testid": "listing-link"})
            if a_tag and "href" in a_tag.attrs:
                href = a_tag["href"]
                complete_url = href if href.startswith("http") else f"https://www.kijiji.ca{href}"
                article_links.append(complete_url)

        pagination_container = soup.find("nav", {"aria-label": "Search Pagination"})
        current_page_li = pagination_container.find("li", {"data-testid": "pagination-list-item-selected"})
        next_page_li = current_page_li.find_next_sibling("li")
        next_page_link = next_page_li.find("a", {"data-testid": "pagination-link-item"}) if next_page_li else None
        next_page_url = next_page_link['href'] if next_page_link and 'href' in next_page_link.attrs else None
        
        if next_page_url:
            initial_content = get_html_content(next_page_url)
        else:
            break

    return article_links

def main() -> pd.DataFrame:
    """Main function to orchestrate scraping of all apartment listings from a given source."""
    all_apartments_df = pd.DataFrame()
    content = get_html_content(KIJIJI_LINK)
    articles = get_apartments_links(content, KIJIJI_LINK)
    for article in tqdm(articles, desc="Processing articles"):
        try:
            article_content = get_html_content(article)
            apartment_df = extract_apartment_data(article, article_content)
            all_apartments_df = pd.concat([all_apartments_df, apartment_df], ignore_index=True)
        except Exception as ex:
            print(f"Error scraping {article}: {str(ex)}")
    return all_apartments_df

if __name__ == "__main__":
    main()
