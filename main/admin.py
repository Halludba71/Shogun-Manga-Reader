from django.contrib import admin
from .models import extension, manga, chapter
# Register your models here.

admin.site.register(manga)
admin.site.register(extension)
admin.site.register(chapter)