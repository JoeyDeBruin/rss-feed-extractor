import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
import csv

# Function to clean and format HTML content
def clean_html_content(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    
    # Handle lists separately for better formatting
    for ul in soup.find_all("ul"):
        for li in ul.find_all("li"):
            li.insert_before("\n- ")  # Add bullet point before list item
        ul.insert_before("\n")  # Add newline before the list
        ul.unwrap()  # Remove the <ul> tag

    for ol in soup.find_all("ol"):
        for i, li in enumerate(ol.find_all("li"), start=1):
            li.insert_before(f"\n{i}. ")  # Add numbered prefix before list item
        ol.insert_before("\n")  # Add newline before the list
        ol.unwrap()  # Remove the <ol> tag

    # Extract and clean text
    text = soup.get_text(separator="\n").strip()
    
    # Remove extra newlines and spaces
    text = re.sub(r'\n+', '\n', text)  # Collapse multiple newlines into one
    text = re.sub(r'\s{2,}', ' ', text)  # Collapse multiple spaces into one

    return text

# Parse the RSS feed
rss_feed = 'rss_feed.xml'  # Replace with your file or URL
tree = ET.parse(rss_feed)
root = tree.getroot()

# Namespace dictionary for RSS fields
namespaces = {
    "content": "http://purl.org/rss/1.0/modules/content/"
}

data = []  # Store extracted data

# Loop through each item in the RSS feed
for item in root.findall(".//item"):
    title = item.find("title").text if item.find("title") is not None else ""
    link = item.find("link").text if item.find("link") is not None else ""
    description = item.find("description").text if item.find("description") is not None else ""
    content = item.find("content:encoded", namespaces)
    raw_html = content.text if content is not None else ""

    # Clean the HTML content
    clean_content = clean_html_content(raw_html)

    # Append to data list
    data.append({
        "title": title.strip(),
        "link": link.strip(),
        "description": description.strip(),
        "content": clean_content
    })

# Define the output CSV file
output_file = "rss_feed_data.csv"

# Save the data to a CSV file
with open(output_file, mode='w', encoding='utf-8', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=["title", "link", "description", "content"])
    writer.writeheader()  # Write the header row
    writer.writerows(data)  # Write the data rows

# Success message
print(f"Data successfully saved to {output_file}")
