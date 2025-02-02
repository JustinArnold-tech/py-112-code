from bs4 import BeautifulSoup
with open("books.xml","r") as infile:
    contents = infile.read()
soup = BeautifulSoup(contents,'html')
titles = soup.find_all('title')
for title in titles:
    print(title.get_text())

from bs4 import BeautifulSoup
with open("books.xml","r") as infile:
    contents = infile.read()
soup = BeautifulSoup(contents,'html')
titles = soup.find_all('title')
for title in titles:
    print(title.get_text())
authors = soup.find_all('author')
for author in authors:
    print(author.get_text())
prices = soup.find_all('price')
for price in prices:
    print(price.get_text())

from bs4 import BeautifulSoup
with open("books.xml","r") as infile:
    contents = infile.read()
soup = BeautifulSoup(contents,'html')
titles = soup.find_all()
for title in titles:
    print(title.get_text())

from bs4 import BeautifulSoup
html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a> and 
<a href="http://example.com/wes" class="brother" id="link3">Wes</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, 'html.parser')
#print(soup.prettify())
mydivs = soup.find_all("a", {"id": "link1"})
for div in mydivs:
    print(div)


import requests
from bs4 import BeautifulSoup
from pprint import pprint
import mysql.connector
from dotenv import dotenv_values

config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}

mydb = mysql.connector.connect(
  host=config['HOST'],
  user=config['USER'],
  password=config['PASSWORD'],
  database="quotes"
)

curr = mydb.cursor()

url = 'http://quotes.toscrape.com/'
result = requests.get(url)
soup = BeautifulSoup(result.content, 'html.parser')

# access quote div block
all_quote_divs = soup.find_all("div",{"class": "quote"})

entries = []
all_tags = set()
for div in all_quote_divs:
    
    #get author , tags and quote text 
    author = div.find("small", {"itemprop":"author"}).get_text()
    tags = [a.get_text() for a in div.find_all("a", {"class":"tag"})]
    
    # | operator same as union() 
    # long hand: all_tags = all_tags.union(tags)
    all_tags |= set(tags)
    
    
    #get rid of special quotation marks 
    quote_text = div.find("span", {"class":"text"}).get_text().replace("“","").replace("”","")
    
    entries.append((quote_text,author,tags))

#make ids for tags 
tags_with_ids = { tag: index + 1 for index, tag in enumerate(all_tags) }
print(tags_with_ids)

# make a table for tags
tags_table_query="""
drop table if exists tags;
create table tags(
    tag_id int primary key not null auto_increment,
    tag_name varchar(100) 
);
"""
quote_book_table_query="""
drop table if exists quote_book; 
create table quote_book(
    quote_id int primary key not null auto_increment,
    quote_text TEXT,
    author varchar(100),
    constraint fk_tag,
    FOREIGN KEY (tag_id) 
        REFERENCES tags(tag_id)
);
"""
insert_into_tags ="""
INSERT INTO tags(tag_name)
VALUES (%s);
"""

insert_into_quote_book="""
INSERT INTO quote_book(quote_text,author,tag_id)
VALUES (%s, %s, %s);
"""

curr.execute(tags_table_query, multi=True)
curr.execute(quote_book_table_query, multi=True)
curr.executemany(insert_into_tags, [(tag, ) for tag in tags_with_ids.keys()])
mydb.commit()

# generate entries with aligned tag ids
vals_to_insert = []
for quote_text, author, tags in entries:
    for tag in tags:
        vals_to_insert.append((quote_text,author,tags_with_ids[tag]))
print(vals_to_insert)


curr.executemany(insert_into_quote_book, vals_to_insert)
mydb.commit()

curr.execute("SELECT * FROM quote_book")
for thing in curr:
    print(thing)
    
curr.execute("SELECT * FROM tags")
for thing in curr:
    print(thing)


mydb.close()
curr.close()