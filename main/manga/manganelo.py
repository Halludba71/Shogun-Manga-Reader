import requests
import re
from bs4 import BeautifulSoup
import os

proxy = "https://proxy.f-ck.me/"

def manga_search(query):
    query = query.replace(" ", "_")
    results = requests.get(f"https://m.manganelo.com/search/story/{query}")
    soup = BeautifulSoup(results.text, "html.parser")
    items = soup.find_all(class_="search-story-item")
    stories = {
        "names":[],
        "links":[],
        "image previews":[],
    }
    for item in items:
        lines = str(item).splitlines()
        stories["names"].append(re.findall(r'<a\s+(?:[^>]*?\s+)?title="([^"]*)',lines[1])[0])
        stories["links"].append(re.findall(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)',lines[1])[0])
    print(stories)


def image_link_grabber(page_url):
    data = requests.get(page_url)
    lines = (data.text).splitlines()
    for line in lines:
        if "container-chapter-reader" in line:
            index = lines.index(line)
    images = lines[index+1]
    soup = BeautifulSoup(images, 'html.parser')
    urls = [proxy+image["src"] for image in soup.findAll("img")]
    return urls
    

def Download_Chapter(urls, Name):
    # Takes in url for a manga page and downloads it
    # for now the images are going to be downloaded in the working directory
    headers = {
        'Referer': "https://readmanganato.com/",  
    }
    path = f"{os.getcwd()}/{Name}"
    if not os.path.exists(path):
        os.mkdir(path)
    for url in urls:
        response = requests.get(url, headers=headers)
        file_name = path + "/" + re.findall(r"/(\d.jpg|\d\d.jpg|\d\d\d.jpg)$", url)[0]
        with open(file_name, "wb") as image:
            image.write(response.content)


# urls = image_link_grabber("https://readmanganato.com/manga-aa951409/chapter-1007")
# print(urls)


# # images = GetImageBinary(urls)
# # print(len(images))
# # print(images[1])
# Download_Chapter(urls, "STAR MARTIAL GOD TECHNIQUE")
# print("Done!")