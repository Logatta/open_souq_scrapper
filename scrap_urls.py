import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://backendentreviable:YUOvAdJC4McHMMgZ@opensouq0.v0yowuq.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))
db = client.get_database("openSouq")
collection = db.get_collection("pages_url")

# URL of the page to scrape
url = input("Enter the section URL: ")

next_page = True
page_num = 1

def create_or_update_document(collection, data):
    existing_document = collection.find_one({'url': data['url']})

    if existing_document is None:
        data['exist'] = False
        collection.insert_one(data)
    else:
        collection.update_one({'_id': existing_document['_id']}, {'$set': {'exist': True}})

while next_page:
    # Send a GET request to the URL
    response = requests.get(url + '?page=' + str(page_num))

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    for div in soup.find_all('div', class_=['mb-32 relative']):
        a_tag = div.find('a')
        if a_tag:
            link = a_tag['href']
            data = {'url': link}
            create_or_update_document(collection, data)

    # Check if there is a next page
    try:
        next_page_link = soup.find('a', {'aria-label': 'page ' + str(page_num + 1)})
        if next_page_link:
            page_num += 1
        else:
            next_page = False
    except TypeError:
        next_page = False
    break

print('Done!')
client.close()
