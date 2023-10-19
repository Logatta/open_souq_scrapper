import re

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from pymongo import MongoClient
from pymongo.server_api import ServerApi


uri = "mongodb+srv://backendentreviable:YUOvAdJC4McHMMgZ@opensouq0.v0yowuq.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))
db = client.get_database("openSouq")

pages_url = db.get_collection("pages_url")
pages_filter = {'exist': False}
urls = pages_url.find(pages_filter)

# Loop over the URLs and scrape the content
for url in urls:
    try:
    # Construct the full URL by adding the open_souq domain
        full_url = 'https://jo.opensooq.com' + url['url'].strip()

        # Set up the Selenium driver and navigate to the URL
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(options=options)

        driver.get(full_url)


        # Get the page source and parse it with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        div = soup.find("div", class_="sc-a97c6d70-5")
        title = div.find("h1").text
        try:
            price = soup.find("span", class_="sc-f9a71135-6").text
        except:
            price = None
        description = soup.select_one("div.sc-2b3ff5d4-1.jKtLVn").text

        image_urls = [img['src'] for img in soup.select('.image-gallery-image')]

        info_div = soup.find('div', class_='sc-23286f3d-0')

        details = {}

        for div in info_div.find_all('div'):
            try:
                label = div.find('p').text
                if label:
                    details[label] = div.find('a').text
            except:
                pass

        # get location
        location = soup.find("a", {"class": "blackColor bold font-18 underLine"}).text

        try:
            anchor_tag = soup.find('a', {'data-ghost': 'map_google'})
            href = anchor_tag['href']
            pattern = r'query=([-\d.]+),([-\d.]+)'
            match = re.search(pattern, href)
            lat, lon = match.groups()
        except:
            lat = None
            lon = None

        # Click button to reveal phone number
        button_xpath = '//*[@id="pageContent"]/div[4]/section/div[1]/div[1]/button[1]'
        button = driver.find_element(By.XPATH, button_xpath)
        button.click()

        phone = driver.find_element(By.XPATH, button_xpath).text

        if not phone:
            # try again
            button.click()
            phone = driver.find_element(By.XPATH, button_xpath).text
        else:
            pass

        data = {
            'title': title,
            'price': price,
            'description': description,
            'image_urls': image_urls,
            'details': details,
            'phone': phone,
            'location': location,
            'lat': lat,
            'lon': lon,
        }
        page_data = db.get_collection("pages_data")
        page_data.insert_one(data)

        driver.quit()
    except Exception as e:
        print(f"fail to scrap {e}", url)
        continue

client.close()
