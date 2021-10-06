import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup


from ebooklib import epub
def epub2thtml(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return chapters

blacklist = [   '[document]',   'noscript', 'header',   'html', 'meta', 'head','input', 'script', "style"]

def chap2text(chap):
    output = ''
    soup = BeautifulSoup(chap, 'html.parser')
    text = soup.find_all(text=True)
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    return output

def thtml2ttext(thtml):
    Output = []
    for html in thtml:
        text =  chap2text(html)
        Output.append(text)
    return Output

def epub2text(epub_path):
    chapters = epub2thtml(epub_path)
    ttext = thtml2ttext(chapters)
    for i in ttext:
        print(i)
        print('\n')
# print(epub2text('book2.epub'))



book = epub.read_epub('book1.epub')
# print(book.get_metadata('DC','title')) # get title of epub
print(book.get_metadata('DC','creator')) # get author name of epub
# print(book.get_metadata('OPF', 'cover')) # get cover
"""
following code is attempt to get cover from epub files
"""
# images = book.get_items_of_type(ebooklib.ITEM_COVER)
# for i in images:
#     print(i)
#
# print(book.get_metadata('OPF', 'cover'))
cover_image = book.get_item_with_id('cover')
print(cover_image)
