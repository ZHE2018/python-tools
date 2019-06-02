from bs4 import BeautifulSoup
import requests

page = 1
url = "http://t66y.com/thread0806.php?fid=20&search=&page=" + str(page)
print(url)
html = requests.get(url).content
soup = BeautifulSoup(html, features="html.parser")
with open('page1.html', 'w', encoding='utf-8') as f:
    f.write(html)
table = soup.find_all('table', id="ajaxtable")
print(str(table))
