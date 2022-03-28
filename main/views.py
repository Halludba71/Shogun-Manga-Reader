from hashlib import new
from threading import currentThread
from turtle import update
from celery import current_app
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import manga, extension, chapter, download, setting, category, mangaCategory
from main.Backend.extensions.extension_list import ext_list
from main.Backend.extensions.download_extensions import download_extension
from main.Backend.extensions.search_manga import search
from main.Backend.extensions.add_manga import newManga
from main.Backend.update import updateChapters, updateLibrary
from win10toast import ToastNotifier
import requests
import sys
import ast
import json
import os
import shutil

# from .reader import * # This line is currently not needed
# Create your views here.

def redirect_view(response):
    response = redirect('/library')
    return response

def library(response):
    library = manga.objects.all
    if response.method == "POST":
            method = response.POST["editLibrary"]
            if method == "updateLibrary":
                libraryUpdating = setting.objects.get(name="libraryUpdating")
                if libraryUpdating.state == False:
                    libraryUpdating.state = True
                    libraryUpdating.save()
                    updateLibrary()
                    libraryUpdating.state = False
                    libraryUpdating.save()
                    
    return render(response, "main/library.html", {'library': library})

def browse(response):
    results = []
    extensions = extension.objects.all()
    if response.method == "GET":
        SearchQuery = response.GET.get('search_box', None)
        if SearchQuery is not None:
            results = search(SearchQuery)
            for k,v in results.items():
                ext = extension.objects.get(name=k)
                for k2, v2 in v.items():
                    if manga.objects.all().filter(title=k2, source=ext.id).exists():
                        mangaInLibrary = manga.objects.get(title=k2, source=ext.id)
                        results[k][k2] = [mangaInLibrary.id, mangaInLibrary.cover, True]

    if response.method == "POST":
        # print(response.POST['mangaInfo'])
        response.session['mangaInfo'] = response.POST['mangaInfo']
        return redirect('/comic/0/0')
    return render(response, "main/browse.html", {"results": results, "extensions": extensions})


def extensions(response):
    if response.method == "POST":
        extension_data = response.POST['extension']
        download_extension(ast.literal_eval(extension_data))
    all_extensions = ext_list()
    installed_extensions = extension.objects.all()
    return render(response, "main/extensions.html", {'installed': installed_extensions, 'all': all_extensions})

def novel(response, id):
    # content = epub2text('E:\Abdullah\Code\Python\Computer Science  NEA\master\Shogan-Manga-Reader-main\main\book2.epub')
    novel = manga.objects.get(id=id)
    return render(response, "main/novel.html", {"novel":novel})

def comic(response, id, inLibrary):
    if inLibrary == 1:
        comic = manga.objects.get(id=id)
        currentCategories = [category.objects.get(id=item.categoryid) for item in mangaCategory.objects.filter(mangaid=id)]
        allCategories = category.objects.all()
        if comic.updating == True:
            toast = ToastNotifier()
            toast.show_toast(
                f'{comic.title} is being updated',
                'Please wait a bit and try again later',
                duration=3,
            )
            return redirect('/library/')
        chapters = chapter.objects.all().filter(comicId=id).exclude(index=-1)
        ordered = chapters.order_by('index')
        if response.method == "POST":
            method = response.POST["editManga"]
            if method == "markRead":
                readChapters = response.POST.getlist("checkbox")
                for chapterId in readChapters:
                    readChapter = chapter.objects.get(id=chapterId)
                    if readChapter.read == False:
                        readChapter.read = True
                        readChapter.lastRead = 0
                        readChapter.save()
                        comic.leftToRead -= 1
                        comic.save()
            if method == "markUnread":
                unreadChapters = response.POST.getlist("checkbox")
                for chapterId in unreadChapters:
                    unreadChapter = chapter.objects.get(id=chapterId)
                    if unreadChapter.read == True:
                        unreadChapter.read = False
                        unreadChapter.lastRead = 0
                        unreadChapter.save()
                        comic.leftToRead += 1
                        comic.save()
            if method == "removeManga":
                for item in chapters:
                    if item.downloaded == True:
                        path = f"{os.getcwd()}\main\static\manga\{comic.id}\{item.id}"
                        if os.path.exists(path):
                            shutil.rmtree(path)
                    item.delete()
                os.remove(f"{os.getcwd()}/main/static/{comic.cover}")
                comic.delete()
                return redirect("/library/")
            if method == "downloadSelected":
                ext = extension.objects.get(id=comic.source)
                sys.path.insert(0, ext.path)
                import source
                selectedChapters = response.POST.getlist("checkbox")
                print(len(selectedChapters))
                for chapterId in selectedChapters:
                    selectedChapter  = chapter.objects.get(id=chapterId)
                    if selectedChapter.downloaded == False:
                        download.objects.create(name=selectedChapter.name, chapterid=selectedChapter.id)
                    if selectedChapter.downloaded == True:
                        selectedChapters.remove(chapterId)
                toast = ToastNotifier()
                toast.show_toast(
                    f'{len(selectedChapters)} Chapter(s) Are Being Downloaded',
                    'Check progress in the downloads page.',
                    duration=3,
                )
                for chapterId in selectedChapters:
                    if selectedChapter.downloaded == False:
                        selectedChapter = chapter.objects.get(id=chapterId)
                        chapterDownloading = download.objects.get(chapterid=selectedChapter.id)
                        images = source.GetImageLinksNoProxy(selectedChapter.url)

                        chapterDownloading.totalPages = len(images)
                        chapterDownloading.save()
                        source.DownloadChapter(images, comic.id, selectedChapter.id, chapterDownloading.id)
            if method == "deleteDownloaded":
                selectedChapters = response.POST.getlist("checkbox")
                for chapterId in selectedChapters:
                    selectedChapter  = chapter.objects.get(id=chapterId)
                    if selectedChapter.downloaded == True:
                        path = f"{os.getcwd()}\main\static\manga\{comic.id}\{chapterId}"
                        if os.path.exists(path):
                            shutil.rmtree(path)
                        selectedChapter.downloaded = False
                        selectedChapter.save()
            
            if method == "showDownloaded":
                chapters = chapter.objects.all().filter(comicId=id, downloaded=True)
            if method == "showRead":
                chapters = chapter.objects.all().filter(comicId=id, read=True)
            if method == "showUnread":
                chapters = chapter.objects.all().filter(comicId=id, read=False)
            if method == "cancelFilter":
                pass
            if method == "updateChapters":
                if comic.updating == False:
                    updated = updateChapters(id)
                    if len(updated) > 0:
                        toast = ToastNotifier()
                        toast.show_toast(
                            f'{comic.title}',
                            f"{','.join(updated)}",
                            duration=4,
                        )
                        leftToRead = len(chapter.objects.filter(comicId=id).exclude(read=True))
                        comic.leftToRead = leftToRead
            if method == "editCategories":
                newCategories = response.POST.getlist("checkbox")
                for item in currentCategories:
                    if item.id not in newCategories:
                        mangaCategoryToDelete = mangaCategory.objects.get(categoryid=item.id, mangaid=id)
                        if mangaCategoryToDelete.categoryid != category.objects.get(name="default").id:
                            mangaCategoryToDelete.delete()
                for categoryId in newCategories:
                    if not mangaCategory.objects.all().filter(categoryid=categoryId, mangaid=id).exists():
                        mangaCategory.objects.create(categoryid=categoryId, mangaid=id)
                currentCategories = [category.objects.get(id=item.categoryid) for item in mangaCategory.objects.filter(mangaid=id)]

        nextChapter = -1
        if len(ordered) > 0:
            nextChapter = ordered[0].index
            for item in ordered:
                if item.read == False:
                    break
                else:
                    nextChapter = item.index
            if nextChapter > 1:
                if nextChapter+1 <= comic.NumChapters:
                    nextChapter = chapter.objects.get(index=nextChapter+1, comicId=comic.id).index
                else:
                    nextChapter = -1
            else:
                nextChapter = chapter.objects.get(index=nextChapter, comicId=comic.id).index
            print(nextChapter)

    elif inLibrary == 0:
        mangaInfo = response.session.get('mangaInfo').split(',')
        ext = extension.objects.get(name=mangaInfo[0])
        if response.method == "POST":
            # newItem = manga.objects.create(name="")
            mangaId = newManga(ext, response.session.get("chapters"), response.session.get("metaData"))
            return redirect(f'/comic/1/{mangaId}')
        sys.path.insert(0, ext.path)
        import source
        comic = source.GetMetadata(mangaInfo[1])
        
        chapters = source.GetChapters(mangaInfo[1])
        # print(mangaInfo[1])
        # print(chapters)
        response.session['chapters'] = chapters
        response.session['metaData'] = comic
        return render(response, "main/browse_comic.html", {"comic":comic, "chapters":chapters})        

    return render(response, "main/comic.html", {"comic":comic, "chapters":ordered.reverse(), "nextChapter": nextChapter, "allCategories": allCategories, "currentCategories":currentCategories})

def read(response, inLibrary, comicId, chapterIndex):
    comic = manga.objects.get(id=comicId)
    if comic.updating == True:
        toast = ToastNotifier()
        toast.show_toast(
            f'{comic.title} is being updated',
            'Please wait a bit and try again later',
            duration=3,
        )
        return redirect('/library/')
    
    currentChapter = chapter.objects.get(comicId=comicId, index=chapterIndex)
    if response.method == "POST":
        data = json.loads(response.body)
        if data["value"] == "Completed":
            currentChapter.lastRead = data['lastRead']
            if currentChapter.read == False:
                currentChapter.read = True
                currentChapter.save()
                comic.leftToRead -= 1
                comic.save()
        if data["value"] == "orientation":
            comic.orientation = data['orientation']
            comic.save()
        if data["value"] == "lastRead":
            currentChapter.lastRead = data['lastRead']
            currentChapter.save()

    if inLibrary == 1:

        if currentChapter.downloaded == True:
            path = f"{os.getcwd()}\main\static\manga\{comicId}\{chapterId}"
            unsorted_images = os.listdir(path)
            images = []
            for i in range(1, len(unsorted_images)+1):
                if "1.png" in unsorted_images:
                    images.append(f"manga/{comicId}/{chapterId}/" + unsorted_images[unsorted_images.index(f"{str(i)}.png")])
                if "1.jpg" in unsorted_images:
                    images.append(f"manga/{comicId}/{chapterId}/" + unsorted_images[unsorted_images.index(f"{str(i)}.jpg")])
        else:
            ext = extension.objects.get(id=comic.source)
            sys.path.insert(0, ext.path)
            import source
            images = source.GetImageLinks(currentChapter.url)
            print(images)

    return render(response, "main/read.html", {"comic": comic, "chapter": currentChapter, "images": images})
    # return render(response, "main/read.html", {"comic": comic, "chapter": chapter})

def downloads(response):
    currentDownloads = download.objects.all()

    return render(response, "main/downloads.html", {"downloads": currentDownloads})

def bypass(response, imageUrl):
    headers = {
        'Referer': "https://readmanganato.com/",
    }
    # r = requests.get(imageUrl, headers=headers)
    imageData = (requests.get(imageUrl, headers=headers)).content
    # print(imageData)
    return HttpResponse(imageData, content_type="image/png")

def settings(response):
    if response.method == "POST":
        method = response.POST["editSetting"]
        if method == "newCategory":
            categoryName = response.POST["categoryName"]
            if category.objects.all().filter(name=categoryName).exists():
                toast = ToastNotifier()
                toast.show_toast(
                    f'Category already exists!',
                    'Category names must be unique',
                duration=3,
                )
            else:
                category.objects.create(name=categoryName)
        if method == "deleteCategory":
            categoryName = response.POST["categoryName"]
            categoryToDelete = category.objects.get(name=categoryName)
            mangaCategory.objects.all().filter(categoryid=categoryToDelete.id).delete()
            categoryToDelete.delete()
    categories = category.objects.all().exclude(name="default")
    return render(response, "main/settings.html", {"categories": categories})