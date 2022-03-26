from main.models import manga, extension, chapter
from win10toast import ToastNotifier
import time
import sys

def updateLibrary():
    updates = []
    library = manga.objects.all()
    for comic in library:
        update = updateChapters(comic.id)
        if len(update) > 0:
            updates.append(comic.title)
            leftToRead = len(chapter.objects.filter(comicId=comic.id).exclude(read=True))
            comic.leftToRead = leftToRead
            comic.save()
    if len(updates) > 0:
        toast = ToastNotifier()
        toast.show_toast(
            f'New Chapters',
            f"{','.join(updates)}",
            duration=4,
        )
def updateChapters(comicId):
    comic = manga.objects.get(id=comicId)
    chapters = chapter.objects.all().filter(comicId=comicId).exclude(index=-1)
    ext = extension.objects.get(id=comic.source)
    sys.path.insert(0, ext.path)
    import source
    print(comic.url)
    newChapters = source.GetChapters(comic.url) # fetches the data for chapters from source
    reversed = newChapters[::-1]
    for currentChapter in chapters:
        currentChapter.index = -1 # changes the index of all of the current chapters to -1
        currentChapter.save()
    for newChapter in newChapters:
        chapter.objects.create(name=newChapter["name"], url=newChapter["url"], comicId=comicId, index=reversed.index(newChapter)+1)
    ## TODO: Need to go through the database, link chapters by name and transfer properties such as downloaded and so on
    chapters = chapter.objects.all().filter(comicId=comicId).exclude(index=-1)
    updated = []
    for newChapter in chapters:
        filtered = chapter.objects.filter(comicId=comicId, name=newChapter.name).order_by('index')
        if len(filtered) > 1:
            read, lastRead, downloaded = filtered[0].read, filtered[0].lastRead, filtered[0].downloaded
            filtered[1].read = read 
            filtered[1].lastRead = lastRead
            filtered[1].downloaded =  downloaded
            filtered[1].save()
            filtered[0].delete()
        else:
            updated.append(filtered[0].name)
    return updated