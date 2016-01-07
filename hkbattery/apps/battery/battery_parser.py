import logging
from time import time
import asyncio
import aiohttp
import bs4

logger = logging.getLogger(__name__)

start = time()

root_url = 'http://www.hobbyking.com/hobbyking/store/'
index_url = 'uh_listCategoriesAndProducts.asp?cwhl=RU&idCategory=86&v=&sortlist=H&LiPoConfig='

sem = asyncio.Semaphore(50)


async def get(url):
    r = await aiohttp.get(url)
    r.soup = bs4.BeautifulSoup(await r.text(), 'lxml')
    return r


async def rounder(num):
    return '%.0f' % round(float(num), 0)


async def catalog_pages():
    logger.info('Parsing catalog pages...')
    r = await get(root_url + index_url)
    nav = r.soup.select('form.paging a')
    return [a.attrs.get('href') for a in nav][:-1]


async def product_pages(page):
    with await sem:
        logger.info('Parsing product pages...')
        r = await get(root_url + page)
    links = r.soup.select('td[colspan="5"] a[style]')
    return [a.attrs.get('href') for a in links]


async def product_data(product_page):
    with await sem:
        r = await get(root_url + product_page)
        logger.info(product_page)
    try:
        name = r.soup.select_one('#productNameWidget').text.replace(' (RU Warehouse)', '').strip()
    except:
        name = '_'
    try:
        pic = r.soup.select('img[id="mainpic1"]')[0].attrs.get('src')
        pic = root_url + pic
    except:
        pic = ''
    try:
        price = r.soup.select('p.productCTABoxPriceUnit')[0].get_text()
        price = price.replace('EU', '')
    except:
        price = 0
    try:
        stock = r.soup.select_one('label.productCtaAnswer').get_text()
        if stock == 'Out of Stock':
            stock = False
        else:
            stock = True
    except:
        stock = ''
    product_data = [root_url + product_page, name, pic, price, stock]
    try:
        specs = r.soup.select('span[id^=prodDataArea_]')[0]
        rows = specs.select('tr')
        for row in rows:
            cols = row.select('td')
            cols = [col.text.strip() for col in cols]
            product_data.append(await rounder([col for col in cols if col][1]))
    except:
        pass
    names = ['link', 'name', 'pic', 'price', 'ru_stock',
             'capacity', 's_config', 'discharge',
             'weight', 'charge', 'length', 'height', 'width']
    return dict(zip(names, product_data))


@asyncio.coroutine
def get_product_pages(catalog_pages):
    result = [product_pages(page) for page in catalog_pages]
    return [(yield from page) for page in asyncio.as_completed(result)]


@asyncio.coroutine
def get_product_data(product_pages):
    result = [product_data(page) for page in product_pages]
    return [(yield from page) for page in asyncio.as_completed(result)]


def parser():
    loop = asyncio.get_event_loop()
    get_catalog_pages = loop.run_until_complete(catalog_pages())
    pages = loop.run_until_complete(get_product_pages(get_catalog_pages))
    pages_flat = [item for sublist in pages for item in sublist]
    result = loop.run_until_complete(get_product_data(pages_flat))
    logger.info(round(time()-start, 2))
    return result


if __name__ == '__main__':
    logging.basicConfig(
            format='%(asctime)s [%(name)s:%(lineno)s] %(levelname)s - %(message)s',
            level=logging.DEBUG)

    print(len(parser()))
