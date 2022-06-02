import requests
import time
from pymongo import MongoClient
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# selenium 設定
options = webdriver.chrome.options.Options()
profile_path = '/Users/fujiwarayuuki/Library/Application Support/Google/Chrome/Default'
driver = webdriver.Chrome("/Users/fujiwarayuuki/chromedriver",options=options)

# mongo 設定
#mongoexport --host="localhost" --port=27017 --db="buyma" --collection="re" --type="csv" --out="ddddd.csv" --fields="ブランド名,商品名,商品URL,型番,テーマ,ライン,関連タグ,販売価格,仕入価格" --noHeaderLine 
#db.dropDatabase();
client = MongoClient('localhost', 27017) # ローカルホストDBに接続。
collection1 = client.buyma.re

base_url = 'https://www.buyma.com'
vuitton_url = 'https://www.buyma.com/r/_LOUIS-VUITTON-ルイヴィトン/-A1000026000/'
dior_url = 'https://www.buyma.com/r/-A1000026000/Dior/'
fendi_url = 'https://www.buyma.com/r/_FENDI-フェンディ/-A1000026000/'
chanel_url = 'https://www.buyma.com/r/_CHANEL-シャネル/-A1000026000/'
diesel_url = 'https://www.buyma.com/r/_DIESEL-ディーゼル/-A1000026000/'
gucci_url = 'https://www.buyma.com/r/_GUCCI-グッチ/-A1000026000/'
celine_url = 'https://www.buyma.com/r/_CELINE-セリーヌ/-A1000026000/'
hermes_url = 'https://www.buyma.com/r/_HERMES-エルメス/-A1000026000/'

brand_url = [vuitton_url, dior_url, fendi_url, chanel_url, diesel_url, gucci_url, celine_url, hermes_url]


def main(url):
    for i in item_list(url):
        item_dict = item_data(i)
        collection1.insert_one(item_dict)
        print(item_dict)

    driver.quit()



def item_list(url):
    time.sleep(1)
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')
    num = 0
    for i in soup.select('li.product '):
        if num <= 19:
            item = i.select_one('div.product_Action').get('item-url')
            item_url = f'{base_url}{item}'
            yield item_url
        num += 1


def item_data(url):
    time.sleep(2)
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')

    # ブランド名
    name = soup.select_one('#s_brand > dd > a').text.replace('\n',"")
    brand_name = name.replace(' ', '')
    print(brand_name)
    # 商品名
    item_name = soup.select_one('#item_h1 > span').text
    print(item_name)
    # 商品U R L
    item_url = url
    print(item_url)
    # 型番
    try:

        item_num = soup.select_one('#s_season > dd > span').text
        print(item_num)
    except:
        item_num = 'なし'
        print(item_num)
    # テーマ
    try:
        item_tema = soup.select_one('#detail_txt > dl:nth-child(4) > dd > a').text
        print(item_tema)
    except:
        item_tema = 'なし'
        print(item_tema)
    # ライン
    try:
        item_line = soup.select_one('#s_model > dd > span > a').text
        print(item_line)
    except:
        item_line = 'なし'
        print(item_line)
    # 関連タグ
    list = []
    for i in soup.select('li.n_common_TagStyle'):
        tag = i.select_one('a').text
        list.append(tag)
    
    if not list:
        item_tag = 'なし'
        print(item_tag) 
    else:
        item_tag = ",".join(list)
        print(item_tag)
    # 販売価格
    item_price = soup.select_one('#abtest_display_pc').text
    print(item_price)
    # 仕入価格
    item_stocking = hp(item_num, brand_name)
    

    item_dict = {
        'ブランド名': brand_name, 
        '商品名': item_name, 
        '商品URL': item_url, 
        '型番': item_num, 
        'テーマ': item_tema, 
        'ライン': item_line, 
        '関連タグ': item_tag, 
        '販売価格': item_price,
        '仕入価格': item_stocking,
        }

    return item_dict



def hp(item_num, brand_name):
    vuitton = 'LouisVuitton(ルイヴィトン)'
    dior = 'Dior(ディオール)'
    fendi = 'FENDI(フェンディ)'
    chanel = 'CHANEL(シャネル)'
    diesel = ''
    gucci = ''
    celine = ''
    hermes = ''

    if brand_name == vuitton:
        if item_num != 'なし':
            item_stocking = vuiton_sc(item_num)
            return item_stocking
        else:
            item_stocking = vuitton
            return item_stocking

    elif brand_name == dior:
        if item_num != 'なし':
            item_stocking = dior_sc(item_num)
            return item_stocking
        else:
            item_stocking = item_num
            return item_stocking

    elif brand_name == fendi:
        if item_num != 'なし':
            item_stocking = fendi_sc(item_num)
            return item_stocking
        else:
            item_stocking = item_num
            return item_stocking

    elif brand_name == chanel:
        if item_num != 'なし':
            item_stocking = chanel_sc(item_num)
            return item_stocking
        else:
            item_stocking = item_num
            return item_stocking

    elif brand_name == diesel:
        pass
    elif brand_name == gucci:
        pass   
    elif brand_name == celine:
        pass  
    elif brand_name == hermes:
        pass  


    
def vuiton_sc(item_num):
    try:
        
        url = 'https://jp.louisvuitton.com/jpn-jp/homepage'
        driver.get(url)
        time.sleep(3)
        wait = WebDriverWait(driver, 10)
        time.sleep(15)
        driver.find_element_by_css_selector('#header > div > div > nav.lv-header__utility > ul > li.lv-header__utility-item.-search > button > span').click()
        driver.find_element_by_css_selector("#searchHeaderInput").send_keys(item_num)
        driver.find_element_by_css_selector("#searchHeaderInput").submit()
        time.sleep(5)

        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'notranslate')))
    
        z = driver.find_element_by_css_selector('div.lv-product-purchase.lv-product-new__purchase > div.lv-product-purchase__price-stock > div > span')
        
        item_stocking = z.text
        return item_stocking

    except:
        item_stocking = 'なし'
        return item_stocking


def dior_sc(item_num):
    base_url = 'https://www.dior.com/ja_jp/products/search?query='
    url = f'{base_url}{item_num}'
    driver.get(url)
    time.sleep(10)
    html = driver.page_source.encode('utf-8')
    time.sleep(1)
    soup = BeautifulSoup(html, 'lxml')
    a = soup.select_one('p.multiline-text.search-results-toolbar-no-results-message')

    if search_confirmation(a):
        item_stocking = soup.select_one('span.price-line').text
        return item_stocking
    
    else:
        item_stocking = 'なし'
        return item_stocking



def fendi_sc(item_num):
    """
    """
    z = item_num
    url = f'https://www.fendi.com/jp-ja/search?q={z}&lang=ja_JP'
    driver.get(url)
    time.sleep(10)
    html = driver.page_source.encode('utf-8')
    time.sleep(1)
    soup = BeautifulSoup(html, 'lxml')

    try:
        item_stocking = soup.select_one('div.price > span > span').text
        return item_stocking
    
    except:
        a = soup.select_one('span.h3.d-block.mb-6').text
        print(a)
        item_stocking = 'なし'
        return item_stocking



def chanel_sc(item_num):
    """
    """
    url = 'https://www.chanel.com/jp/'

    driver.get(url)
    time.sleep(10)
    driver.find_element_by_css_selector('li.is-hidden-s').click()
    time.sleep(10)
    driver.find_element_by_css_selector("#searchInput").send_keys(item_num.replace(' ',""))
    driver.find_element_by_css_selector("button.button.search__button.search__submit.js-search-submit").click()
    time.sleep(5)
  
    html = driver.page_source.encode('utf-8')
    time.sleep(1)
    soup = BeautifulSoup(html, 'lxml')

    try:
        a = soup.select_one('p.product-details__price').text

        v = a.replace(' ',"")
        q = v.replace('*', "")
        item_stocking = q.replace('\n',"")

        return item_stocking

    except:
        item_stocking = 'なし'
        return item_stocking


def diesel_sc(item_num):
    """
    """



def gucci_sc(item_num):
    """
    """

def celine_sc(item_num):
    """
    """


def hermes_sc(item_num):
    """
    """



def search_confirmation(a):
    """
    一致する商品があればTrueなければFalseを返す。
    """
   
    if a is None:
        return True
    else:
        return False


#item_data('https://www.buyma.com/item/69494032/')
#item_data('https://www.buyma.com/item/82722679/')
#item_data('https://www.buyma.com/item/81501726/')

main(chanel_url)