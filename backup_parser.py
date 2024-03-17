def get_menu(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    menu_data = {}

    sections = soup.find_all("div", attrs={"data-testid": "restaurant-menu-section"})

    for section in sections:
        section_title = section.find(
            "h3", attrs={"data-testid": "menuSection-title"}
        ).text.strip()
        menu_items = get_menu_items(section)
        menu_data[section_title] = menu_items

    return menu_data


def get_menu_items(section):
    items_container = section.find_next_sibling(
        "div", attrs={"data-testid": "menu-items-container"}    )

    menu_items = []
    while items_container:
        items = items_container.find_all(
            "article", attrs={"data-testid": "restaurant-menu-item"}
        )
        for item in items:
            name = (
                item.find("h6", class_="u-text-ellipsis").text.strip()
                if item.find("h6", class_="u-text-ellipsis")
                else "No Name"
            )            description = (
                item.find("span", class_="menuItemNew-description--truncate-3").text.strip()
                if item.find("span", class_="menuItemNew-description--truncate-3")
                else "No Description"
            )
            price = extract_price(item)
            menu_items.append({"name": name, "description": description, "price": price})

        items_container = items_container.find_next_sibling(
            "div", attrs={"data-testid": "menu-items-container"}
        )

    return menu_items


def extract_price(item):
    price_span = item.find("span", attrs={"data-testid": "menu-item-price"})
    if price_span:
        price_text = price_span.text.split("+")[0].strip()
        return price_text
    return "N/A"
