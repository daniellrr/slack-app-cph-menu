from bs4 import BeautifulSoup
from datetime import datetime
import locale
import requests

# Set locale to Danish to match day names
locale.setlocale(locale.LC_TIME, 'da_DK.UTF-8')

url = 'https://www.foodandco.dk/besog-os-her/restauranter/ku/sondre-campus/'

# Use the requests library to fetch the web page content
response = requests.get(url)

# Now, response.text contains the HTML content
html_content = response.text

# Function to get the Danish name for the current day of the week
def get_today_danish():
    return datetime.now().strftime('%A')  # '%A' gives the full weekday name

# Simulated HTML content (replace this with `requests.get(url).text` for actual fetching)


soup = BeautifulSoup(html_content, 'html.parser')

def extract_menu_for_today(soup):
    today_danish = get_today_danish()
    # Find all paragraphs with <strong> tags, which denote days of the week
    day_tags = soup.find_all('p', string=lambda text: text and today_danish in text)

    menu_items = []
    for day_tag in day_tags:
        # Extract menu items that follow the day tag
        for sibling in day_tag.find_next_siblings():
            if sibling.name == 'p' and not sibling.find('strong'):
                menu_items.append(sibling.get_text(strip=True))
            elif sibling.find('strong'):  # Stop if another day is encountered
                break

    return menu_items

def main():
    menu_items = extract_menu_for_today(soup)
    if menu_items:
        print(f"Menu for {get_today_danish()}: \n")
        for item in menu_items:
            print(f"- {item}")

main()

# Function to extract the menu for a given restaurant section
def extract_menu(restaurant_section):
    today = datetime.now().strftime("%A").lower()  # Get the current day in lowercase (e.g., 'monday')
    menu = {}  # Dictionary to hold the menu items

    # Find all day sections within the restaurant section
    day_sections = restaurant_section.find_all(['h6', 'p'], style="text-align: center;")
    current_day = None

    for section in day_sections:
        # Check if the section is a day header (e.g., <h6 style="text-align: center;"><strong>Mandag</strong></h6>)
        if section.name == 'h6':
            day_name = section.text.strip().lower()
            if today in day_name:
                current_day = day_name  # Set the current day if it matches today
            else:
                current_day = None  # Reset current day if it's a different day
        elif current_day and section.text.strip():  # If it's the current day and the section has menu items
            menu_item = section.text.strip()
            if current_day in menu:
                menu[current_day].append(menu_item)
            else:
                menu[current_day] = [menu_item]

    return menu

# Find all restaurant sections in the HTML
restaurant_sections = soup.find_all("div", class_="ContentBlock")

for index, restaurant_section in enumerate(restaurant_sections, start=1):
    menu = extract_menu(restaurant_section)
    if menu:
        today_danish = get_today_danish()
        for day, items in menu.items():
            #print(f"{day.capitalize()}:")
            for item in items:
                print(f"- {item}")
        print("\n")
