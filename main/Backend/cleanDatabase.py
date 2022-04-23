from main.models import manga, chapter, mangaCategory, setting
from pathlib import Path
import shutil
import os

PLATFORM = os.name
if PLATFORM == "nt":
    from win10toast import ToastNotifier

def checkDatabase():
    library = manga.objects.all()
    deletedManga = []
    for comic in library:
        if chapter.objects.all().filter(comicId=comic.id, index=-1).exists():
            deletedManga.append(comic.title)
            allChapters = chapter.objects.filter(comicId=comic.id)
            for item in allChapters:
                if item.downloaded == True:
                    path = Path.cwd() / "main" / "static" / "manga" / str(comic.id) / str(item.id)
                    if os.path.exists(path):
                        shutil.rmtree(path)
                item.delete()
            os.remove(Path.cwd() / "main" / "static" / comic.cover)
            mangaCategory.objects.filter(mangaid=comic.id).delete()
            comic.delete()
    if len(deletedManga) > 0:
        if PLATFORM == "nt":
            toast = ToastNotifier()
            toast.show_toast(
                'The following manga were removed from your library',
                f"{', '.join(deletedManga)}",
                duration=4,
            )
    libraryUpdating = setting.objects.get(name="libraryUpdating")
    libraryUpdating.state = False
    libraryUpdating.save()

