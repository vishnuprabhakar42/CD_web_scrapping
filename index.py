import requests
from bs4 import BeautifulSoup
import pandas as pd

# Target URL
url = "https://www.top10vpn.com/best-vpn-for-india/"

# Send GET request to fetch the webpage content
response = requests.get(url)
if response.status_code != 200:
    print("Failed to retrieve the website. Status code:", response.status_code)
    exit()

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Lists to store scraped data
logos = []
names = []
contents = []
ratings = []
links = []

# Scraping data
# Locate elements using appropriate tags and classes
vpn_items = soup.find_all('div', class_='container')  # Replace 'vpn-card' with the actual class for each VPN item
for item in vpn_items:
    # Scrape logo URL
    logo_tag = item.find('img', class_='jsx-3803777512 ppc__provider-logo')  # Replace 'vpn-logo' with the actual logo class
    logo = logo_tag['src'] if logo_tag else 'N/A'
    logos.append(logo)
    
    # Scrape name
    name_tag = item.find('h3', class_='jsx-3803777512')  # Replace 'vpn-title' with the actual title class
    name = name_tag.text.strip() if name_tag else 'N/A'
    names.append(name)
    
    # Scrape content
    content_tag = item.find('p', class_='vpn-description')  # Replace 'vpn-description' with the actual description class
    content = content_tag.text.strip() if content_tag else 'N/A'
    contents.append(content)
    
    # Scrape rating
    rating_tag = item.find('span', class_='jsx-3803777512')  # Replace 'vpn-rating' with the actual rating class
    rating = rating_tag.text.strip() if rating_tag else 'N/A'
    ratings.append(rating)
    
    # Scrape link
    link_tag = item.find('a', class_='button button--chevron button--chevron-variant')  # Replace 'vpn-link' with the actual link class
    link = link_tag['href'] if link_tag else 'N/A'
    links.append(link)

# Create a DataFrame to organize the scraped data
data = {
    'Logo': logos,
    'Name': names,
    'Content': contents,
    'Rating': ratings,
    'Link': links
}
df = pd.DataFrame(data)

# Save the data to an Excel file
df.to_excel('vpn_data.xlsx', index=False)

print("Data scraped successfully and saved to 'vpn_data.xlsx'")
