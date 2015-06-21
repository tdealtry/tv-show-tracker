from main import *
from lxml import html
from bs4 import BeautifulSoup

test()

tables = get_tables("files/tables.html")
seasons = [season for season in tables]


html = read_html("files/tables.html")
parsed_html = BeautifulSoup(html)

print(parsed_html.body.find('tr', attrs={'class' : 'vevent'}).text)


