# OpenSouq Web Scraping Documentation

## Overview

This documentation provides an explanation of a Python script used to scrape data from the OpenSouq website. The script is designed to scrape product listings, including titles, prices, descriptions, image URLs, contact details, and geographical location data. The script is divided into two parts: URL scraping and page content scraping.

## Requirements

Before running the script, make sure you have the following Python packages installed:

- `requests` version 2.31.0
- `selenium` version 4.14.0
- `beautifulsoup4` version 4.12.2
- `pymongo` version 4.5.0

You can install these packages using pip:

```bash
pip install requests==2.31.0 selenium==4.14.0 beautifulsoup4==4.12.2 pymongo==4.5.0
```

## Script Components

### 1. URL Scraping (`scrap_urls.py`)

#### Purpose
This part of the script is responsible for scraping URLs of product listings in a specified category on the OpenSouq website.

#### Usage

1. Run the script `scrap_urls.py`.
2. Enter the section URL when prompted.
3. The script will start scraping the URLs of product listings for the specified category and save them in a MongoDB database.

### 2. Page Content Scraping (`scrap_pages.py`)

#### Purpose
This part of the script is designed to scrape the content of individual product listings using the URLs collected in the first part.

#### Usage

1. Run the script `scrap_pages.py`.
2. The script will fetch URLs from the MongoDB database (from the first part) that have not been processed yet.
3. For each URL, the script navigates to the product page, collects various details, and saves the data in a MongoDB collection named `pages_data`.

## MongoDB Configuration

The script connects to a MongoDB database to store the scraped data. To configure the MongoDB connection, update the `uri` variable in both parts of the script with your MongoDB Atlas connection string.

## Data Scraped

The script collects the following information from each product listing:

- Title
- Price
- Description
- Image URLs
- Details (various product details)
- Phone number
- Location
- Latitude and Longitude

## Error Handling

The script includes basic error handling to skip over any pages that encounter issues during scraping. Failed URLs are printed in the console for further investigation.

## Headless Browser

Selenium is used with a headless browser, which means that the web scraping is done without opening a visible web browser window.

## Notes

- The script is designed to scrape data from the OpenSouq website. It may not work with other websites.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
