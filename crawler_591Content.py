def connect_until_success(url):
    import requests
    header = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
              "Accept-Encoding": "gzip, deflate, br",
              "Accept-Language": "zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4",
              "Cache-Control": "max-age=0",
              "Connection": "keep-alive",
              "Cookie": "PHPSESSID=6bi7bnrv70rduoug42ptjdkrk3; new_rent_list_kind_test=1; T591_TOKEN=6bi7bnrv70rduoug42ptjdkrk3; _gat_tw591=1; _ga=GA1.3.1725785438.1503324510; _gid=GA1.3.659177335.1503324510; _gat=1; _dc_gtm_UA-97423186-1=1; c10f3143a018a0513ebe1e8d27b5391c=1; urlJumpIp=1; urlJumpIpByTxt=%E5%8F%B0%E5%8C%97%E5%B8%82; 591_new_session=eyJpdiI6IkhOelIwYUFrMU1KMmRON0NiTkxNN2c9PSIsInZhbHVlIjoiWUFcL2ZGN2U2eGVxNlpmVjZUVERWUDN6T0lFZFNvWUo0YjB6REEycjVES1BQVmFpVEhwcHpHZ3hKYlBMTUFpSjd2QUZkdnFuSERNSHY1ZURhVVh0dUh3PT0iLCJtYWMiOiJmY2VjMzNlNDhhODVjZGQ5YmY4YWMzYzU3MmUxNjUyYjgzN2NmYjM3NTg0MDcyM2IyN2FmNjVjMzdiMGY4OTBjIn0%3D; _ga=GA1.4.1725785438.1503324510; _gid=GA1.4.659177335.1503324510; _gat_UA-97423186-1=1",
              "Host": "rent.591.com.tw",
              "Upgrade-Insecure-Requests": "1",
              "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
              }

    count = 10
    while count > 0:
        try:
            res = requests.get(url, headers=header, timeout=2)
            count = 0
            break
        except Exception as e:
            if count == 1:
                time.sleep(count * 0.1)
            count -= 1
    return res


def get_content(url):
    try:
        rentDict = {}
        res = connect_until_success(url)
        soup = BeautifulSoup(res.text, 'lxml')
        info = soup.select("#propNav > a['href']")
        city = info[2].text
        area = info[3].text
        type = info[4].text
        title = soup.select('.houseInfoTitle')[0].text
        # 標題
        address = soup.select('span.addr')[0].text
        # 地址
        price = soup.select('div.price > i')[0].text.split(' 元/月')[0].replace(',', '')
        # 租金
        houseInfo = soup.select('ul.attr > li')
        if info[2].text == "車位":
            square = houseInfo[0].text.split('\xa0')[3].split('坪')[0]
            floor = ""
            style = ""

        elif houseInfo[0].text.split('\xa0')[0] == "坪數":

            if houseInfo[1].text.split('\xa0')[0] == "權狀坪數":
                square = houseInfo[0].text.split('\xa0')[3].split('坪')[0]
                floor = houseInfo[2].text.split('\xa0')[3].split('/')[0]
                totfloor = houseInfo[2].text.split('\xa0')[3].split('/')[1]
                style = houseInfo[3].text.split('\xa0')[3]
            else:
                square = houseInfo[0].text.split('\xa0')[3].split('坪')[0]
                floor = houseInfo[1].text.split('\xa0')[3].split('/')[0]
                totfloor = houseInfo[1].text.split('\xa0')[3].split('/')[1]
                style = houseInfo[2].text.split('\xa0')[3]

        elif houseInfo[0].text.split('\xa0')[0] == "格局":
            if houseInfo[2].text.split('\xa0')[0] == "權狀坪數":
                square = houseInfo[1].text.split('\xa0')[3].split('坪')[0]
                floor = houseInfo[3].text.split('\xa0')[3].split('/')[0]
                totfloor = houseInfo[3].text.split('\xa0')[3].split('/')[1]
                style = houseInfo[4].text.split('\xa0')[3]
            else:
                square = houseInfo[1].text.split('\xa0')[3].split('坪')[0]
                floor = houseInfo[2].text.split('\xa0')[3].split('/')[0]
                totfloor = houseInfo[2].text.split('\xa0')[3].split('/')[1]
                style = houseInfo[3].text.split('\xa0')[3]

        else:
            None
        seller = soup.select('.avatarRight')[0].text.strip().replace("（", '(').split('(')[0]
        identity = \
        soup.select('.avatarRight')[0].text.strip().replace("（", '(').replace("）", ')').split(')')[0].split('(')[1]
        if identity == "屋主聲明：仲介勿擾":
            identity = "屋主"
        elif identity == "仲介，收取服務費" or "仲介，不須服務費":
            identity = "仲介"
        else:
            None

        phoneSoup = soup.select_one("span.num")

        if len(phoneSoup) == 1 and phoneSoup.text == "":
            for img in phoneSoup:
                phone = img['src']
            soldout = 0
        elif len(phoneSoup) == 1 and phoneSoup.text != "":
            phone = phoneSoup.text
            soldout = 0

        else:
            phone = ""
            soldout = 1


        if len(soup.select('div.lifeBox > p')) == 2:
            traffic = soup.select('div.lifeBox > p')[1].text.replace("附近交通：", "").split('； ')
        else:
            traffic = ""
        rentDict['url'] = url
        rentDict['title'] = title
        rentDict['seller'] = seller
        rentDict['identity'] = identity
        rentDict['phone'] = phone
        rentDict['price'] = price
        rentDict['type'] = type
        rentDict['floor'] = floor
        rentDict['totfloor'] = totfloor
        rentDict['square'] = square
        rentDict['address'] = address
        rentDict['city'] = city
        rentDict['area'] = area
        rentDict['style'] = style
        rentDict['traffic'] = str(traffic)
        rentDict['soldout'] = str(soldout)


    except Exception as e:
        print('There is get_content trouble in {},{} '.format(url, e))
    return rentDict


def drop_table(save_path):
    try:
        db = sqlite3.connect(save_path)
        cur= db.cursor()
        cur.execute("DROP TABLE IF EXISTS rent_temp2;")
        db.commit()
    except Exception as e:
        db.rollback()
        print("There is trouble in dropping table {}".format(e))
    finally:
        db.close()

"""------------------------------------------------------------------------------------"""
def create_table(save_path):
    try:
        db = sqlite3.connect(save_path)
        cur= db.cursor()
        cur.execute("CREATE TABLE rent_temp2(url text, title text, seller text, identity text, phone text, price int, type text, floor text,totfloor text, square int, address text, city text, area text, style text, traffic text,soldout int);")
        db.commit()
    except Exception as e:
        db.rollback()
        signal = str("There is trouble in creating database {} {} ".format(e))
        print("There is trouble in creating database {} {} ".format(e))






def add_to_sqlite(rentDict,save_path):
    if rentDict != {}:
        # print(rentDict)
        url   = rentDict['url']
        title = rentDict['title']
        seller = rentDict['seller']
        identity =rentDict['identity']
        phone = rentDict['phone']
        price = rentDict['price']
        type = rentDict['type']
        floor = rentDict['floor']
        totfloor = rentDict['totfloor']
        square= rentDict['square']
        address= rentDict['address']
        city =rentDict['city']
        area=rentDict['area']
        style=rentDict['style']
        traffic=rentDict['traffic']
        soldout =rentDict['soldout']

        try:
            conn = sqlite3.connect(save_path)
            cur = conn.cursor()
            cur.execute('INSERT INTO rent_temp2 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                        (url, title, seller, identity, phone, price, type, floor,totfloor, square, address, city, area, style, traffic,soldout))
            conn.commit()

        except Exception as e:
            print('at data {} mysql server cannot connect: {}'.format(url, e))
            conn.rollback()
        finally:
            conn.close()


def main(url, save_path):
    alreadyCrawled = 0
    rentDict = get_content(url)
    add_to_sqlite(rentDict, save_path)
    alreadyCrawled +=1
    time.sleep(0.2)
    if alreadyCrawled % 100 ==0:
        printstring = ('*****we have crawled ' + str(alreadyCrawled) + ' pages *****')
        sys.stdout.write('\r' + printstring)

from bs4 import BeautifulSoup
import sys
import time
import sqlite3
import os
if __name__ == "__main__":
    open_path = "./591_test.csv"
    save_path = "./591.sqlite3"
    drop_table(save_path)
    create_table(save_path)
    with open(open_path, 'r',encoding='utf-8')as fr:
        for idx, url in enumerate(fr):
            url = url.strip()
            main(url, save_path)

    print('\n' + 'crawling finished!')