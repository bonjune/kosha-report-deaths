# Parse the HTML files, and
# Store the result into sqlite db file for later use

from bs4 import BeautifulSoup
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine

FILE_NAMES = [
  'deaths_0.html',
  'deaths_500.html',
  'deaths_1000.html',
]

def parse_file(filename: str):
  with open(filename, 'r') as f:
    soup = BeautifulSoup(f, 'html.parser')

    table = soup.find('tbody')

    for element in table.find_all('tr'):
      uid: str = element.find('td', {'class': 'board-list-uid'}).text.strip()
      title: str = element.find('td', {'class': 'board-list-title'}).text.strip()
      report_date: str = element.find('td', {'class': 'board-list-date'}).text.strip()

      yield {'uid': uid, 'title': title, 'date': report_date}

def get_articles():
  for file_name in FILE_NAMES:
    for article in parse_file(file_name):
      if article['uid'] == '공지':
        continue
      yield article

engine = create_engine('sqlite:///kosha-deaths.db')
metadata = MetaData()

articles = Table(
  'articles',
  metadata,
  Column('uid', Integer, primary_key=True),
  Column('title', String),
  Column('date', String)
)

metadata.drop_all(engine)
metadata.create_all(engine)

data = list(get_articles())

print(f'{len(data)} articles available')

with engine.connect() as conn:
  conn.execute(articles.insert(), data)
  conn.commit()
