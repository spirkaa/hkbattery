import logging
from multiprocessing.pool import ThreadPool
from time import time
from mechanicalsoup import Browser

logger = logging.getLogger(__name__)
logging.getLogger("requests").setLevel(logging.WARNING)

start = time()

root_url = 'http://www.hobbyking.com/hobbyking/store/'
index_url = 'uh_listCategoriesAndProducts.asp?cwhl=RU&idCategory=86&v=&sortlist=H&LiPoConfig='
csv_name = 'battery_full_catalog'


def rounder(num):
    return '%.0f' % round(float(num), 0)


def mechbrowser(url):
    browser = Browser()
    return browser.get(root_url + url)


def get_catalog_page_urls():
    logger.info('Parsing catalog page URLs...')
    r = mechbrowser(index_url)
    nav = r.soup.select('form.paging a')
    return [a.attrs.get('href') for a in nav][:-1]


def get_product_page_urls(page):
    logger.info('Parsing product page URLs...')
    r = mechbrowser(page)
    links = r.soup.select('td[colspan="5"] a[style]')
    return [a.attrs.get('href') for a in links]


def get_product_data(product_page_url):
    r = mechbrowser(product_page_url)
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
    product_data = [root_url + product_page_url, name, pic, price, stock]
    try:
        specs = r.soup.select('span[id^=prodDataArea_]')[0]
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
