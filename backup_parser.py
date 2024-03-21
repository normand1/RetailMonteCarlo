from bs4 import BeautifulSoup
import json


def read_html_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return html_content


# Function to extract price information from a menu item element
def extract_price(item):
    price_span = item.find("span", attrs={"data-testid": "menu-item-price"})
    if price_span:
        price_text = price_span.text.split("+")[0].strip()
        return price_text
    return "N/A"


# Function to gather all menu items from the HTML content
def get_menu_items(soup):
    menu_items = []
    items = soup.find_all("article", attrs={"data-testid": "restaurant-menu-item"})
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


# Updated main function to parse the menu from HTML content
def get_menu_updated(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    menu_data = {}

    # Fetching all items since the association to sections is not directly clear
    all_menu_items = get_menu_items(soup)

    # Assuming sections are identified correctly but bypassing direct association for this demonstration
    sections = soup.find_all("div", attrs={"data-testid": "restaurant-menu-section"})
    for section in sections:
        section_title = section.find(
            "h3", attrs={"data-testid": "menuSection-title"}
        ).text.strip()
        # Directly associating all found items to each section for demonstration purposes
        menu_data[section_title] = all_menu_items

    return menu_data


html_content = read_html_from_file("example2.html")
menu_data = get_menu_updated(html_content)
with open("menu_data.json", "w") as f:
    json.dump(menu_data, f, indent=4)
