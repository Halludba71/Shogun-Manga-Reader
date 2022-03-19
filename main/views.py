from hashlib import new
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from .models import manga, extension, chapter
from main.Backend.extensions.extension_list import ext_list
from main.Backend.extensions.download_extensions import download_extension
from main.Backend.extensions.search_manga import search
from main.Backend.extensions.add_manga import newManga
import requests
import sys
import ast
# from .reader import * # This line is currently not needed
# Create your views here.


def redirect_view(response):
    response = redirect('/library')
    return response

def library(response):
    library = manga.objects.all
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
        chapters = chapter.objects.all().filter(comicId=id)
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
                    item.delete()
                comic.delete()
                return redirect("/library/")

        ordered = chapters.order_by('index')
        if len(ordered) > 0:
            nextChapter = ordered[0].index
            for item in ordered:
                if item.read == False:
                    break
                else:
                    nextChapter = item.index
            if nextChapter+1 <= comic.NumChapters:
                nextChapter = chapter.objects.get(index=nextChapter+1, comicId=comic.id).id
            else:
                nextChapter = -1
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

    return render(response, "main/comic.html", {"comic":comic, "chapters":chapters, "nextChapter": nextChapter})

def read(response, inLibrary, comicId, chapterId):
    currentChapter = chapter.objects.get(id=chapterId)
    comic = manga.objects.get(id=comicId)
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
        ext = extension.objects.get(id=comic.source)
        sys.path.insert(0, ext.path)
        import source
        images = source.GetImageLinks(currentChapter.url)

    return render(response, "main/read.html", {"comic": comic, "chapter": currentChapter, "images": images})
    # return render(response, "main/read.html", {"comic": comic, "chapter": chapter})

def bypass(response, imageUrl):
    headers = {
        'Referer': "https://readmanganato.com/",
    }
    # r = requests.get(imageUrl, headers=headers)
    imageData = (requests.get(imageUrl, headers=headers)).content
    # print(imageData)
    return HttpResponse(imageData, content_type="image/png")
    # return HttpResponse("hello")