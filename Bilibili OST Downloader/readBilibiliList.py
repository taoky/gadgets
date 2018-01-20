import requests
from bs4 import BeautifulSoup

r = requests.get("https://www.bilibili.com/video/av2520368/") # change it to what you want to download
r.encoding = "utf-8"
soup = BeautifulSoup(r.text, "html.parser")

print(soup.find(id="plist").get_text())
