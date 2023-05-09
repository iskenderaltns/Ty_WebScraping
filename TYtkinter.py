from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import requests


class TrendyolData:
    def __init__(self, product, amountData, OrderBy, FileName) -> None:
        self.product = product
        self.fileName = FileName
        self.OrderBy = OrderBy
        self.AmountData = amountData
        self.url_trendyol = f'https://www.trendyol.com/sr?q={self.product}&qt={self.product}self&st={self.product}&os=1&sst={self.OrderBy}'
        self.headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
        self.driver = None
        self.scroll_pause_time = 1
        self.scroll_times = 10

    def start_driver(self):
        options = Options()
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        service = Service('/path/to/chromedriver')
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(1)
        self.driver.maximize_window()

    def stop_driver(self):
        if self.driver:
            self.driver.quit()

    def changePage(self):
        self.start_driver()
        for i in range(self.AmountData*2):
            url = self.url_trendyol
            url += str('&pi=' + str(i + 1))
            try:
                self.trend(url)
            except:
                continue
        self.stop_driver()
        return True

    def trend(self, x):

        self.driver.get(x)
        try:
            products = WebDriverWait(self.driver, 2).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                     '#search-app > div > div.srch-rslt-cntnt > div.srch-prdcts-cntnr > div:nth-child(4) > div:nth-child(1) > div > div'))

            )

        except UnboundLocalError or TimeoutError or Exception:
            return False

        price_product = []
        title_product = []
        description_product = []
        addr_product = []
        for h in products:
            try:

                title_element = h.find_element(By.CSS_SELECTOR, 'div.p-card-chldrn-cntnr.card-border > a > div.product-down > div > div > div > span.prdct-desc-cntnr-ttl')
                title = title_element.get_attribute('title')
                title_product.append(title)
                description_element = h.find_element(By.CSS_SELECTOR, 'div.p-card-chldrn-cntnr.card-border > a > div.product-down > div > div > div > span.prdct-desc-cntnr-name.hasRatings')
                description = description_element.get_attribute('title')
                description_product.append(description)
                try:
                    price = h.find_element(By.CSS_SELECTOR,
                                       'div.p-card-chldrn-cntnr.card-border > a > div.product-down > div.price-promotion-container > div > div.prc-box-dscntd').text
                except:
                    price = h.find_element(By.CSS_SELECTOR,
                                           'div.p-card-chldrn-cntnr.card-border > a > div.product-down > div.product-price > div > div > div.prc-box-dscntd').text
                price_product.append(price)

                addr_element = h.find_element(By.CSS_SELECTOR, 'div.p-card-chldrn-cntnr.card-border > a')
                addr = addr_element.get_attribute('href')
                addr_product.append(addr)

            except:
                continue


        if title_product:
            self.save_sql(title_product, description_product, price_product, addr_product)

    def save_sql(self, b, d, p, a):
        with sqlite3.connect(str(self.fileName) + '.db') as db:
            cursor = db.cursor()
            table = """CREATE TABLE IF NOT EXISTS TRENDYOLALL(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                       Brand INTEGER, Description VARCHAR(200), Price INTEGER, Addr TEXT);"""

            cursor.execute(table)
            for i in range(len(b)):
                cursor.execute('''INSERT INTO TRENDYOLALL(Brand, Description, Price, Addr) VALUES (?, ?, ?, ?)''',
                               (b[i], d[i], p[i], a[i]))
                db.commit()


