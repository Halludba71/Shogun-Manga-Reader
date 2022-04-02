import requests
import re
from bs4 import BeautifulSoup
import os
from main.models import chapter, download, extension
from main.Backend.IfOnline import connected
extensionId = extension.objects.get(name="Manganato").id
proxy = f"/bypass/{extensionId}/"

def SearchManga(query):
    """
    Searches Manganato for a specifc manga
    """
    if connected() == True:
        try:
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
        except:
            return -1
    else:
        return -1

def GetChapters(manga_url):
    """
    Gets chapter info for a specific manga
    info includes name and upload date
    """
    if connected() == True:
        try:
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
        except:
            return -1
    else:
        return -1

def GetMetadata(manga_url):
    """
    Gets all metadata for a certain manga
    """
    if connected() == True:
        try:
            request = requests.get(manga_url)
            soup = BeautifulSoup(request.text, "html.parser")
            name = re.findall(r'<h1>(.*?)</h1>', str(soup.find("h1")))[0]
            cover = re.findall(r'src="(.*?)"',str(soup.find(class_="info-image")))[0]
            author = ", ".join(re.findall(r'>(.*?)</a>', str(soup.find(class_="info-author").parent.parent)))
            description = soup.findAll(class_="panel-story-info-description")[0].text
            mangaInfo = {}
            mangaInfo["name"] = name
            mangaInfo["url"] = manga_url
            mangaInfo["cover"] = cover
            mangaInfo["author"] = author
            mangaInfo["description"] = description
            return mangaInfo
        except:
            return -1
    else:
        return -1

def GetImageLinks(page_url):
    """
    scrapes links for all images of a specific chapter
    """
    if connected() == True:
        try:
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
        except:
            return []
    else:
        return []

def GetImageLinksNoProxy(page_url):
    """
    scrapes links for all images of a specific chapter
    """
    if connected() == True:
        try:
            data = requests.get(page_url)
            lines = (data.text).splitlines()
            for line in lines:
                if "container-chapter-reader" in line:
                    index = lines.index(line)
            images = lines[index+1]
            soup = BeautifulSoup(images, 'html.parser')
            urls = [image["src"] for image in soup.findAll("img")]
            # urls = [proxy+image["src"] for image in soup.findAll("img")] - the previous url
            return urls
        except:
            return []
    else:
        return []

def DownloadChapter(urls, comicid, chapterId, downloadId):
    # Takes in url for a manga page and downloads it
    # for now the images are going to be downloaded in the working directory
    headers = {
        'Referer': "https://readmanganato.com/",
    }
    path = f"{os.getcwd()}\main\static\manga\{comicid}\{chapterId}"
    if not os.path.exists(path):
        os.makedirs(path)

    for index,url in enumerate(urls):
        response = requests.get(url, headers=headers)
        if response.ok:
            file_name = f"{path}/{index+1}.{url[len(url)-3::]}"
            print(file_name)
            if download.objects.all().filter(id=downloadId).exists() == False:
                break
            chapterToDownload = download.objects.get(id=downloadId)
            with open(file_name, "wb") as image:
                image.write(response.content)

            chapterToDownload.downloaded += 1
            chapterToDownload.save()
        else:
            download.objects.get(id=downloadId).delete()
            return True

    if download.objects.all().filter(id=downloadId).exists() == False:
        return False
    chapterToDownload = chapter.objects.get(id=chapterId)
    chapterToDownload.downloaded = True
    chapterToDownload.save()
    download.objects.get(id=downloadId).delete()
    return False
