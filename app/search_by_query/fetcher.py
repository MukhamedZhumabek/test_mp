import asyncio
import aiohttp

import json
import time

from collections import deque
from logging import getLogger

from .manager import save_parsed_data

logger = getLogger('app.fetcher')

url = ('https://search.wb.ru/exactmatch/ru/common/v4/search?&query={}'
       '&curr=rub&dest=-1257786&regions=80,64,38,4,115,83,33,68,70,69,30,86,75,40,1,66,48,110,31,22,71,114,111'
       '&resultset=catalog&sort=popular&spp=0&suppressSpellcheck=false&limit=300&page={}')


async def get_by_query(query: str = 'куртка', count: int = 10):

    pages = deque([i for i in range(1, count + 1)])  # pages queue

    while pages:
        page = pages.popleft()  # remove current page from queue
        start_time = time.time()
        logger.info(f'Start fetching {query}:{page}')
        logger.info(f'pages to fetching {pages}')
        async with aiohttp.ClientSession() as session:
            async with session.get(url.format(query, page)) as response:
                if response.status == 200:  # parse response data
                    text = await response.text()
                    data = json.loads(text)
                    data['query'] = str(query) # add additional info to parsed data
                    data['page'] = int(page)
                elif response.status == 429:
                    logger.warning(f'To many requests when try to get page {query}:{page}')
                    pages.append(page)  # return current page from queue
                    await asyncio.sleep(10)
                    continue
                else:
                    logger.error(f'Unexpected response from API: {response}')

        logger.info(f'Fetching {query}:{page} completed in {(time.time() - start_time):.2f} seconds')

        await save_parsed_data(data)  # save parsed data to db
        logger.info('No more pages for fetching. Stopping fetcher.')