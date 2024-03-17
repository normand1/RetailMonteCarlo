import requests
from bs4 import BeautifulSoup


class WebsiteScraper:
    @staticmethod
    def scrape_website(url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            # Customize this selector based on actual website structures
            prices = soup.find_all("div", class_="price")
            return [price.text for price in prices]
        except Exception as e:
            print(f"Could not scrape {url}: {e}")
            return []
