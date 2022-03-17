import requests
import re
from bs4 import BeautifulSoup
import os
import base64

proxy = "/bypass/"

def SearchManga(query):
    """
    Searches Manganato for a specifc manga
    """
    query = query.replace(" ", "_")
    results = requests.get(f"https://readmanganato.com/search/story/{query}")
    soup = BeautifulSoup(results.text, "html.parser")
    items = soup.find_all(class_="search-story-item")
    # Results = { "manga": link, image  ,...}
    Results = {}
    for item in items:
        lines = str(item).splitlines()
        Name = re.findall(r'<a\s+(?:[^>]*?\s+)?title="([^"]*)',lines[1])[0]
        Results[Name] = [re.findall(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)',lines[1])[0], re.findall(r'<img\s+(?:[^>]*?\s+)?src="([^"]*)',lines[2])[0], False]
    return(Results)

def GetChapters(manga_url):
    """
    Gets chapter info for a specific manga
    info includes name and upload date
    """
    request = requests.get(manga_url)
    soup = BeautifulSoup(request.text, "html.parser")
    results = soup.find(class_="row-content-chapter").find_all("li")
    Chapters = []
    for result in results:
        lines = str(result).splitlines()
        ChapterName = re.findall(r'>(.*?)</a>', lines[1])[0]
        ChapterLink = re.findall(r'href="(.*?)"', lines[1])[0]
        # Date = re.findall(r'>(.*?)</span>', lines[3])[0]
        # print(ChapterLink)
        Chapters.append({"name":ChapterName, "url": ChapterLink})
    return(Chapters)

def GetMetadata(manga_url):
    """
    Gets all metadata for a certain manga
    """

    request = requests.get(manga_url)
    soup = BeautifulSoup(request.text, "html.parser")
    name = re.findall(r'<h1>(.*?)</h1>', str(soup.find("h1")))[0]
    cover = re.findall(r'src="(.*?)"',str(soup.find(class_="info-image")))[0]
    author = re.findall(r'>(.*?)</a>', str(soup.findAll(class_="table-value")[1]))[0]
    description = soup.findAll(class_="panel-story-info-description")[0].text
    mangaInfo = {}
    mangaInfo["name"] = name
    mangaInfo["url"] = manga_url
    mangaInfo["cover"] = cover
    mangaInfo["author"] = author
    mangaInfo["description"] = description

    return mangaInfo

def GetImageLinks(page_url):
    """
    scrapes links for all images of a specific chapter
    """
    data = requests.get(page_url)
    lines = (data.text).splitlines()
    for line in lines:
        if "container-chapter-reader" in line:
            index = lines.index(line)
    images = lines[index+1]
    soup = BeautifulSoup(images, 'html.parser')
    urls = [proxy+image["src"] for image in soup.findAll("img")]
    # urls = [proxy+image["src"] for image in soup.findAll("img")] - the previous url
    return urls


def DownloadChapter(urls, Name):
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

def imageToBase64(url):
    headers = {
        'Referer': "https://readmanganato.com/",
    }
    r = requests.get(url, headers=headers)
    src = (f"data:{r.headers['Content-Type']};base64, {(base64.b64encode(r.content)).decode('UTF-8')}")
    return src

# print(GetChapters("https://readmanganato.com/manga-aa951409"))