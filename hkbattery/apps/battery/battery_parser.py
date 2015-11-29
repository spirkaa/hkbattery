import logging
from multiprocessing.pool import ThreadPool
from time import time
import mechanicalsoup

logger = logging.getLogger(__name__)
logging.getLogger("requests").setLevel(logging.WARNING)

start = time()

root_url = 'http://www.hobbyking.com/hobbyking/store/'
index_url = 'uh_listCategoriesAndProducts.asp?cwhl=RU&idCategory=86&v=&sortlist=H&LiPoConfig='
csv_name = 'battery_full_catalog'


def rounder(num):
    return '%.0f' % round(float(num), 0)


def mechbrowser(url):
    browser = mechanicalsoup.Browser()
    return browser.get(root_url + url)


def get_catalog_page_urls():
    logger.info('Parsing catalog page URLs...')
    response = mechbrowser(index_url)
    nav = response.soup.select('form.paging a')
    return [a.attrs.get('href') for a in nav][:-1]


def get_product_page_urls(page):
    logger.info('Parsing product page URLs...')
    response = mechbrowser(page)
    links = response.soup.select('td[colspan="5"] a[style]')
    return [a.attrs.get('href') for a in links]


def get_product_data(product_page_url):
    response = mechbrowser(product_page_url)
    name = response.soup.h1.get_text().replace(' (RU Warehouse)', '').strip()
    try:
        pic = response.soup.select('img[id="mainpic1"]')[0].attrs.get('src')
        pic = root_url + pic
    except:
        pic = ''
    try:
        price = response.soup.select('#price_lb')[0].get_text()
        price = price.replace('EU', '')
    except:
        price = None
    try:
        stock = response.soup.select('#pstock2')[0].get_text()
        if stock == '10+':
            stockbar = response.soup.select('#stockbar')[0].attrs.get('style')
            stock = rounder(stockbar.replace('width: ', '').replace('%', ''))
        elif stock == 'BK':
            stock = '0'
    except:
        stock = ''
    product_data = [root_url + product_page_url, name, pic, price, stock]
    try:
        specs = response.soup.select('span[id^=prodDataArea_]')[0]
        rows = specs.select('tr')
        for row in rows:
            cols = row.select('td')
            cols = [col.text.strip() for col in cols]
            product_data.append(rounder([col for col in cols if col][1]))
    except:
        pass
    names = ['link', 'name', 'pic', 'price', 'ru_stock',
             'capacity', 's_config', 'discharge',
             'weight', 'charge', 'length', 'height', 'width']
    return dict(zip(names, product_data))


def links():
    logger.info('Collect links...')
    catalog_page_urls = get_catalog_page_urls()
    with ThreadPool(8) as pooli:
        product_page_urls = pooli.map(get_product_page_urls, catalog_page_urls)
        return [item for sublist in product_page_urls for item in sublist]


def parser():
    product_page_urls = links()
    logger.info('Collect data...')
    with ThreadPool(8) as pool:
        results = pool.map(get_product_data, product_page_urls)
        logger.info('It took %d seconds.', round(time()-start, 2))
        return results
