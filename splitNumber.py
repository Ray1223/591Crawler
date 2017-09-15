def download_photo(idx, url, filePath):
    global fileName
    global row
    res = requests.get("http:" + row[4])
    if res.status_code == 200:
        fileName = "{}.png".format(idx)
        with open(filePath+fileName, 'wb') as f:
            f.write(res.content)
    else:
        None
    return fileName


def cut_number(fileName,filePath,savePath):
    pil_image = PIL.Image.open(filePath+fileName).convert('RGB')
    # 圖片顏色轉換
    open_cv_image = numpy.array(pil_image)
    imgray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # 抓到圖片邊界
    cnts = sorted([(c, cv2.boundingRect(c)[0]) for c in contours], key=lambda x: x[1])
    # 將圖片array放入cnts
    ary = []
    for (c, _) in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        # 抓取"數字"的長寬
        if w >= 7 and h == 20:
            ary.append((x, y, w, h))


    ct = int(time.mktime(datetime.now().timetuple()))
    for idx, (x, y, w, h) in enumerate(ary):
        roi = open_cv_image[y:y + h, x:x + w]
        thresh = roi.copy()
        plt.imshow(thresh)
        plt.savefig(savePath+'{}_{}.png'.format(ct, idx + 1), dpi=100)
    plt.close('all')


def main():
    global fileName
    global row
    sqlite3_path = "./581.sqlite3"
    get_query = "select * from rent_temp;"
    filePath = "./number_test/"
    savePath = "./number/"
    splitNo = 20
    if os.path.exists(filePath):
        shutil.rmtree(filePath)
    os.mkdir(filePath)
    # 清空資料夾

    with sqlite3.connect(sqlite3_path) as conn:
        cur = conn.cursor()
        for idx, row in enumerate(cur.execute(get_query)):
            if idx % 10 == 0:
                print("目前已經分割第{}份".format(idx))
            if idx < splitNo:
                try:
                    download_photo(idx, row[4], filePath)
                    cut_number(fileName, filePath,savePath)
                except:
                    pass

            else:
                break
    print("所有數字已經分割完畢!")

import cv2
import matplotlib.pyplot as plt
import sqlite3
import numpy
from PIL import Image
from bs4 import BeautifulSoup
import PIL
import requests
import time
import os
from datetime import datetime
import shutil

if __name__=="__main__":
    main()