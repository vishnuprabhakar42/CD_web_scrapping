import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page to scrape
url = "https://www.top10vpn.com/best-vpn-for-india/"

# Send a GET request to fetch the raw HTML content
response = requests.get(url)

# Prepare lists to store extracted data
vpn_names = []
text_elements = []
scores = []
website_urls = []

# If request was successful, parse the HTML content
if response.status_code == 200:
    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table containing the VPN data
    table = soup.find('table', class_='jsx-4100803555 table-default ppc__table')  # Adjust the class based on actual site
    
    # Find all tr tags (rows) inside the table, excluding the header row
    rows = table.find_all('tr', class_='jsx-3803777512 ppc__table-row')[0:6]  # Extract rows from 2nd to 6th
    
    for row in rows:
        # Extract VPN Name from the image alt attribute (assuming it's inside the row)
        vpn_name_img = row.find('img', alt=True)  # Find the image with alt attribute
        vpn_name = vpn_name_img['alt'] if vpn_name_img else 'Not found'
        
        # Extract all list and paragraph elements for the VPN (assuming these are in <li> or <p>)
        text_elements_row = row.find_all(['li', 'p'])  # Extract both <li> and <p> tags
        text_list = [element.text.strip() for element in text_elements_row]  # Clean and store text
        
        # Extract the score (usually in a <span> tag)
        score = row.find('span')  # Find the span tag containing the score
        score = score.text.strip() if score else 'Not found'
        
        # Extract the generic website URL (in the <a> tag)
        website_url = row.find('a', href=True)  # Find the anchor tag with href
        website_url = website_url['href'] if website_url else 'Not found'
        
        # Append the extracted data to the lists
        vpn_names.append(vpn_name)
        text_elements.append(', '.join(text_list))  # Join features or descriptions into a single string
        scores.append(score)
        website_urls.append(website_url)

# Create a DataFrame from the lists
data = {
    'VPN Name': vpn_names,
    'Text Elements': text_elements,
    'rank': scores,
    'Website URL': website_urls
}

df = pd.DataFrame(data)

# Save the data to an Excel file
df.to_excel('vpn_data.xlsx', index=False)

print("Data saved to vpn_data.xlsx")