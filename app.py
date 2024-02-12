from bs4 import BeautifulSoup
import datetime
import requests

url = 'https://www.foodandco.dk/besog-os-her/restauranter/ku/sondre-campus/'

# Use the requests library to fetch the web page content
response = requests.get(url)

# Now, response.text contains the HTML content
html_content = response.text

# Use BeautifulSoup to parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Get the current day in Danish (adjust the list based on your requirements or use a library)
days = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag"]
current_day = days[datetime.datetime.now().weekday()]

def print_menu_for_today(soup, day):
    # Find all restaurant sections
    restaurant_sections = soup.find_all('div', class_='ContentBlock')

    for section in restaurant_sections:
        # Find the restaurant name
        restaurant_name_h3 = section.find('h3', style="text-align: center;")
        if restaurant_name_h3:
            restaurant_name = restaurant_name_h3.get_text(strip=True)
            print(f"Restaurant: {restaurant_name}")

            restaurant_description_h4 = section.find('h4', style="text-align: center;")
            if restaurant_description_h4:
              restaurant_description = restaurant_description_h4.get_text(strip=True)
              print(f"{restaurant_description}\n")

            # Check if the day's menu is present
            day_heading = section.find('h6', string=day, style="text-align: center;")
            if day_heading:
                # Get all the menu items for the day
                menu_items = day_heading.find_all_next('p', style="text-align: center;")
                for item in menu_items:
                    # Check if we've reached the next day to stop printing
                    if item.find_previous('h6') != day_heading:
                        break
                    print(item.get_text(strip=True))
                print("\n")  # Add a newline for readability between restaurants

# Call the function with the current day
print_menu_for_today(soup, current_day)
