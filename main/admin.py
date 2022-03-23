from django.contrib import admin
from .models import extension, manga, chapter, categorie, mangaCategorie, download
# Register your models here.

admin.site.register(manga)
admin.site.register(extension)
admin.site.register(chapter)
admin.site.register(categorie)
admin.site.register(mangaCategorie)
admin.site.register(download)