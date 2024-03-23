from competition_maps.google_places_finder import GooglePlacesFinder
from scraper.website_scraper import WebsiteScraper


class CoffeeShopPriceFinder:
    def __init__(self, api_key):
        self.places_finder = GooglePlacesFinder(api_key)
        self.scraper = WebsiteScraper()

    def find_prices(
        self,
        location,
        locationType,
        radius=1000,
    ):
        shops = self.places_finder.find_shops(location, radius, locationType)
        for shop in shops:
            details = self.places_finder.get_place_details(shop["place_id"])
            website = details.get("website", "Website not available")
            print(f"Shop: {shop['name']}, Website: {website}")
            if website != "Website not available":
                prices = self.scraper.scrape_website(website)
                print(f"Prices found: {prices}")
            else:
                print("No website available for scraping.")
