import os

from dotenv import load_dotenv

from coffee_shop_price_finder import CoffeeShopPriceFinder

load_dotenv()

LOCATION = "40.712776,-74.005974"


def main():
    price_finder = CoffeeShopPriceFinder(os.getenv("API_KEY"))
    price_finder.find_prices(LOCATION, locationType="cafe")


if __name__ == "__main__":
    main()
