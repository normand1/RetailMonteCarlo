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


def get_item(browser, id):
    try:
        button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.ID, id))
        )
        browser.execute_script("arguments[0].click();", button)
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "menuItemModal-options"))
        )
    except Exception as e:
        print(f"Error clicking on or waiting for item options to load: {e}")
        return {}

    innerHTML = browser.page_source
    html = BeautifulSoup(innerHTML, "html.parser")

    _options = {}
    options = html.find_all("div", class_="menuItemModal-options")
    for option in options:
        name = option.find(class_="menuItemModal-choice-name").text
        choices = option.find_all(
            "span", class_="menuItemModal-choice-option-description"
        )
        # Assume choices[0] exists and contains text with " + " for this example
        _choices = (
            {
                choice.text.split(" + ")[0]: choice.text.split(" + ")[1]
                for choice in choices
            }
            if " + " in choices[0].text
            else [choice.text for choice in choices]
        )
        _options[name] = _choices
    return _options


def get_menu(url):
    print("Scraping menu...")
    browser = uc.Chrome()
    browser.get(url)

    # Wait for the menu items to be loaded
    WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[@data-testid='menu-item']"))
    )

    html_source = browser.page_source
    soup = BeautifulSoup(html_source, "html.parser")

    menu_data = {}

    sections = soup.find_all("div", attrs={"data-testid": "restaurant-menu-section"})

    for section in sections:
        section_title = section.find(
            "h3", attrs={"data-testid": "menuSection-title"}
        ).text.strip()
        menu_items = get_menu_items(section)
        menu_data[section_title] = menu_items

    browser.quit()

    # Generate the file name based on the URL
    url_parts = re.findall(r"https?://(?:www\.)?(.+?)/(.+?)/(\d+)", url)
    if url_parts:
        website, restaurant_name, restaurant_id = url_parts[0]
        # Remove invalid characters from the restaurant name
        restaurant_name = re.sub(r'[<>:"/\\|?*]', "_", restaurant_name)
        file_name = f"{website}_{restaurant_name}_{restaurant_id}_menu.json"
    else:
        file_name = "menu_data.json"

    # Create the directory structure based on the current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    directory = os.path.join("scraped_data", current_date)
    os.makedirs(directory, exist_ok=True)

    # Save the menu data to a JSON file within the directory
    file_path = os.path.join(directory, file_name)
    with open(file_path, "w") as file:
        json.dump(menu_data, file, indent=4)

    print(f"Menu data saved to {file_path}")

    return menu_data


def get_menu_items(section):  # -> list:
    items_container = section.find_next_sibling(
        "div", attrs={"data-testid": "menu-items-container"}
    )

    if items_container:
        items = items_container.find_all(
            "article", attrs={"data-testid": "restaurant-menu-item"}
        )
    else:
        items = []

    menu_items = []
    for item in items:
        name = (
            item.find("h6", class_="u-text-ellipsis").text.strip()
            if item.find("h6", class_="u-text-ellipsis")
            else "No Name"
        )
        description = (
            item.find("span", class_="menuItemNew-description--truncate-3").text.strip()
            if item.find("span", class_="menuItemNew-description--truncate-3")
            else "No Description"
        )
        price = extract_price(item)
        menu_items.append({"name": name, "description": description, "price": price})

    return menu_items


def extract_price(item):
    price_span = item.find("span", attrs={"data-testid": "menu-item-price"})
    if price_span:
        price_text = price_span.text.split("+")[0].strip()
        return price_text
    return "N/A"


# Adjustments:
# - Improved selectors based on the structure you provided.
# - Ensured accurate identification and extraction of menu item names and prices.
# - Added comments and simplified logic for readability and maintainability.

get_menu(input("Grubhub Link? "))
# example link: 'https://www.grubhub.com/restaurant/insomnia-cookies-76-pearl-st-new-york/295836'
