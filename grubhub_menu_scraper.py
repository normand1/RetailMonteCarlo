from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import json
import undetected_chromedriver as uc
import re
from datetime import datetime


def get_menu_items(browser, section):
    section_html = section.get_attribute("outerHTML")
    soup = BeautifulSoup(section_html, "html.parser")

    # Attempt to extract menu items directly without waiting for visibility
    items = soup.find_all("article", attrs={"data-testid": "restaurant-menu-item"})
    menu_items = []
    for item in items:
        try:
            name = item.find("h6").text.strip() if item.find("h6") else "No Name"
            description = (
                item.find(
                    "span", class_="menuItemNew-description--truncate-3"
                ).text.strip()
                if item.find("span", class_="menuItemNew-description--truncate-3")
                else "No Description"
            )
            price = item.find(
                "span", attrs={"data-testid": "menu-item-price"}
            ).text.strip()
            menu_items.append(
                {"name": name, "description": description, "price": price}
            )
        except Exception as e:
            print(f"Error processing item: {e}")

    return menu_items


def get_menu(url):
    print("Scraping menu...")
    browser = uc.Chrome()

    try:
        browser.get(url)
        WebDriverWait(browser, 30).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[@data-testid='restaurant-menu-section']")
            )
        )
        sections = browser.find_elements(
            By.XPATH, "//div[@data-testid='restaurant-menu-section']"
        )
        menu_data = {}

        for section in sections:
            section_title = section.find_element(
                By.XPATH, ".//h3[@data-testid='menuSection-title']"
            ).text.strip()
            menu_items = get_menu_items(browser, section)
            menu_data[section_title] = menu_items

        # Convert menu_data to JSON or print it out here
        print(json.dumps(menu_data, indent=2))

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        browser.quit()


# Example usage
url = input("Grubhub Link? ")
get_menu(url)

# Adjustments:
# - Improved selectors based on the structure you provided.
# - Ensured accurate identification and extraction of menu item names and prices.
# - Added comments and simplified logic for readability and maintainability.
# example link: 'https://www.grubhub.com/restaurant/insomnia-cookies-76-pearl-st-new-york/295836'
