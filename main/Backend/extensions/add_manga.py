import sys
from main.models import manga, chapter
import requests
import hashlib
import os

def newManga(ext, chapters, metaData):
    # sys.path.insert(0, ext.path)
    # import source
    print(metaData["url"])
    numChapters = len(chapters)
    ## TODO: download Image
    request = requests.get(metaData["cover"])
    fileName = "covers/" + hashlib.md5(request.content).hexdigest() + metaData["cover"][ len(metaData["cover"]) -4::]
    path = f"{os.getcwd()}/main/static/"
    with open(path+fileName, "wb") as cover:
        cover.write(request.content)

    newManga = manga.objects.create(title=metaData["name"], url=metaData["url"], cover=fileName, description=metaData["description"], source=ext.id, author=metaData["author"], orientation="vertical", NumChapters=numChapters)
    reversed = chapters[::-1]
    for item in chapters:
        chapter.objects.create(name=item["name"], url=item["url"], comicId=newManga.id, index=reversed.index(item)+1)
    return newManga.id