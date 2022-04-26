from main.models import extension
import sys
import os

PLATFORM = os.name
if PLATFORM == "nt":
    from win10toast import ToastNotifier


def search(SearchQuery):
    extensions = extension.objects.all()
    results = {}
    failedSearches = []
    for ext in extensions:
        sys.path.insert(0, ext.path) #./main/Backend/extensions/Manganato/
        import source
        searchResult = source.SearchManga(SearchQuery)
        if searchResult == -1:
            failedSearches.append(ext.name)
            results[ext.name] = []
        else:
            results[ext.name] = searchResult
    if len(failedSearches) > 0:
        if PLATFORM == "nt":
            toast = ToastNotifier()
            toast.show_toast(
                f'Search Failed for {len(failedSearches)} source(s)',
                'Check your internet connection or try again',
                duration=3,
            )
    return results
