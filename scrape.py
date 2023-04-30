# Get the HTML files from KOSHA death report articles

import httpx

ARTICLE_LIMIT = 500

def get_url(offset: int):
  if offset % ARTICLE_LIMIT != 0:
    raise ValueError(f'Offset ({offset}) must be a multiple of ARTICLE_LIMIT ({ARTICLE_LIMIT})')

  url = f'https://www.kosha.or.kr/kosha/report/kosha_news.do?mode=list&&articleLimit={ARTICLE_LIMIT}&article.offset={offset}'
  return url

for offset in range(0, 1500, 500):
  res = httpx.get(url=get_url(offset))

  res.raise_for_status()

  with open(f'deaths_{offset}.html', 'w+') as f:
    f.write(res.text)