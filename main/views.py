from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from .models import manga, extension, chapter
from main.Backend.extensions.extension_list import ext_list
from main.Backend.extensions.download_extensions import download_extension
from main.Backend.extensions.search_manga import search
import requests
# from .reader import * # This line is currently not needed
# Create your views here.


def redirect_view(response):
    response = redirect('/library')
    return response

def library(response):
    library = manga.objects.all
    return render(response, "main/library.html", {'library': library})

def browse(response):
    if response.method == "GET":
        SearchQuery = response.GET.get('search_box', None)
        if SearchQuery is not None:
            search(SearchQuery)
    return render(response, "main/browse.html", {})


def extensions(response):
    if response.method == "POST":
        import ast
        extension_data = response.POST['extension']
        download_extension(ast.literal_eval(extension_data))
    all_extensions = ext_list()
    print(type(all_extensions))
    installed_extensions = extension.objects.all
    return render(response, "main/extensions.html", {'installed': installed_extensions, 'all': all_extensions})

def novel(response, id):
    # content = epub2text('E:\Abdullah\Code\Python\Computer Science  NEA\master\Shogan-Manga-Reader-main\main\book2.epub')
    novel = manga.objects.get(id=id)
    return render(response, "main/novel.html", {"novel":novel})

def comic(response, id, inLibrary):
    if inLibrary == 1:
        comic = manga.objects.get(id=id)
        chapters = chapter.objects.all().filter(comicId=id)

    elif inLibrary == 0:
        pass
    return render(response, "main/comic.html", {"comic":comic, "chapters":chapters})

def read(response, inLibrary, comicId, chapterIndex):
    currentChapter = chapter.objects.get(index=chapterIndex)
    comic = manga.objects.get(id=comicId)
    if response.method == "POST":
        data = json.loads(response.body)
        if data["value"] == "Completed":
            currentChapter.lastRead = data['lastRead']
            currentChapter.read = True
            currentChapter.save()
        if data["value"] == "orientation":
            comic.orientation = data['orientation']
            comic.save()
        if data["value"] == "lastRead":
            currentChapter.lastRead = data['lastRead']
            currentChapter.save()

    if inLibrary == 1:
        # comic = manga.objects.get(id=comicId)
        # chapters = comic.chapters_to_arr()
        # chapter = chapters[chapterId - 1]
        # ext = extension.objects.get(id=comic.source)
        # import sys
        # sys.path.insert(0,ext.path)
        # import source
        # images = source.GetImageLinks(chapter["url"])

        ext = extension.objects.get(id=comic.source)
        import sys
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