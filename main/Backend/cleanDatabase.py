from main.models import manga, chapter, mangaCategory, setting
from win10toast import ToastNotifier
import shutil
import os

def checkDatabase():
    library = manga.objects.all()
    deletedManga = []
    for comic in library:
        if chapter.objects.all().filter(comicId=comic.id, index=-1).exists():
            deletedManga.append(comic.title)
            allChapters = chapter.objects.filter(comicId=comic.id)
            for item in allChapters:
                if item.downloaded == True:
                    path = f"{os.getcwd()}\main\static\manga\{comic.id}\{item.id}"
                    if os.path.exists(path):
                        shutil.rmtree(path)
                item.delete()
            os.remove(f"{os.getcwd()}/main/static/{comic.cover}")
            mangaCategory.objects.filter(mangaid=comic.id).delete()
            comic.delete()
    if len(deletedManga) > 0:
        toast = ToastNotifier()
        toast.show_toast(
            'The following manga were removed from your library',
            f"{', '.join(deletedManga)}",
            duration=4,
        )
    libraryUpdating = setting.objects.get(name="libraryUpdating")
    libraryUpdating.state = False
    libraryUpdating.save()

