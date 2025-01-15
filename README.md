# Substack RSS Feed Parser and HTML Cleaner

This script parses an RSS feed from Substack, extracts data from each item, cleans the HTML content, and saves the results into a CSV file.

## Features

- Parses RSS feeds in XML format.
- Extracts and cleans HTML content from `<content:encoded>` fields using BeautifulSoup.
- Handles ordered (`<ol>`) and unordered (`<ul>`) lists for better formatting.
- Outputs the cleaned and structured data to a CSV file.

## Requirements

- Python 3.6+
- `beautifulsoup4`
- `lxml`
