import requests
from bs4 import BeautifulSoup

page_url = "https://mangasee123.com/read-online/Naruto-chapter-1.html"
data = requests.get(page_url)
soup  = BeautifulSoup(data.text, "html.parser")
lines = (data.text).splitlines()
items = soup.find_all('img')
for item in items:
    print(item)
