from bs4 import BeautifulSoup
from datetime import datetime
import locale
import requests

# Set locale to Danish to match day names
locale.setlocale(locale.LC_TIME, 'da_DK.UTF-8')

url = 'https://www.foodandco.dk/besog-os-her/restauranter/ku/sondre-campus/'

# Use the requests library to fetch the web page content
response = requests.get(url)
html_content = response.text

# Slack webhook URL


def get_today_danish():
    return datetime.now().strftime('%A')

soup = BeautifulSoup(html_content, 'html.parser')

def extract_menu_for_today(soup):
    today_danish = get_today_danish()
    day_tags = soup.find_all('p', string=lambda text: text and today_danish in text)
    menu_items = []
    for day_tag in day_tags:
        for sibling in day_tag.find_next_siblings():
            if sibling.name == 'p' and not sibling.find('strong'):
                menu_items.append(sibling.get_text(strip=True))
            elif sibling.find('strong'):
                break
    return menu_items

def extract_menu(restaurant_section):
    today = datetime.now().strftime("%A").lower()
    menu = {}
    day_sections = restaurant_section.find_all(['h6', 'p'], style="text-align: center;")
    current_day = None
    for section in day_sections:
        if section.name == 'h6':
            day_name = section.text.strip().lower()
            if today in day_name:
                current_day = day_name
            else:
                current_day = None
        elif current_day and section.text.strip():
            menu_item = section.text.strip()
            if current_day in menu:
                menu[current_day].append(menu_item)
            else:
                menu[current_day] = [menu_item]
    return menu

def main():
    output = ""  # Initialize an empty string to collect the output
    menu_items = extract_menu_for_today(soup)
    if menu_items:
        output += f"Menu for {get_today_danish()}:\n\n"
        for item in menu_items:
            output += f" {item}\n"
        output += "\n"

    restaurant_sections = soup.find_all("div", class_="ContentBlock")
    for restaurant_section in restaurant_sections:
        menu = extract_menu(restaurant_section)
        if menu:
            for day, items in menu.items():
                for item in items:
                    output += f" {item}\n"
            output += "\n"

    # Send the output to Slack
    payload = {"text": output}
    response = requests.post(slack_webhook_url, json=payload)
    if response.status_code == 200:
        print("Message sent to Slack successfully.")
    else:
        print(f"Failed to send message to Slack. Status code: {response.status_code}")

main()
