from django.contrib import admin
from .models import extension, manga, chapter, download, setting, category, mangaCategory
# Register your models here.

admin.site.register(manga)
admin.site.register(extension)
admin.site.register(chapter)
admin.site.register(category)
admin.site.register(mangaCategory)
admin.site.register(download)
admin.site.register(setting)