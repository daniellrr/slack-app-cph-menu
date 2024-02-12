from bs4 import BeautifulSoup
from datetime import datetime
import requests
import locale

# Set locale to Danish to match day names and possibly week numbers
locale.setlocale(locale.LC_TIME, 'da_DK.UTF-8')

# Function to get the Danish name for the current day of the week
def get_today_danish():
    return datetime.now().strftime('%A')  # '%A' gives the full weekday name

# Fetch the webpage content
url = 'https://www.foodandco.dk/besog-os-her/restauranter/ku/sondre-campus/'
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

def extract_menus(soup):
    today_danish = get_today_danish()
    menus = {}

    # Find all restaurant sections, assuming they're denoted by specific headings or div classes
    restaurant_sections = soup.find_all("div", class_="ContentBlock")

    for section in restaurant_sections:
        # Attempt to find the restaurant name within the section
        name_tag = section.find(['h3', 'h4'])
        if name_tag:
            restaurant_name = name_tag.get_text(strip=True)

            # Look for today's menu within the section
            today_menu_tag = section.find(lambda tag: tag.name == 'h6' and today_danish.lower() in tag.get_text().lower())
            if today_menu_tag:
                menu_items = []
                for sibling in today_menu_tag.find_next_siblings():
                    if sibling.name == 'p' and sibling.get_text(strip=True):
                        menu_items.append(sibling.get_text(strip=True))
                    # Stop if another day is encountered
                    elif sibling.name == 'h6':
                        break
                if menu_items:
                    menus[restaurant_name] = menu_items

    return menus

def main():
    menus = extract_menus(soup)
    if menus:
        for restaurant, items in menus.items():
            print(f"{restaurant} Menu for Today:")
            for item in items:
                print(f"- {item}")
            print("\n")
    else:
        print("No menus found for the current day.")

main()
