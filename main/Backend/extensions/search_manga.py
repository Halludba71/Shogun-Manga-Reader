from main.Backend.extensions.Manganato.source import SearchManga
from main.models import extension
import os
import subprocess
import sys


def search(SearchQuery):
    extensions = extension.objects.all()
    for ext in extensions:
        sys.path.insert(0, ext.path) #./main/Backend/extensions/Manganato/
        import source
        print(source.SearchManga(SearchQuery))
# def search(Query):
#     print(os.getcwd())
