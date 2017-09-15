def download_photo(idx, url, saveNumPath):
    import os
    import shutil
    import requests

    if os.path.exists(saveNumPath):
        shutil.rmtree(saveNumPath)
    os.mkdir(saveNumPath)
    #清空資料夾
    res  = requests.get("http:"+row[4])
    if res.status_code == 200:
        fileName = "{}.png".format(idx)
        with open(saveNumPath+fileName,'wb') as f:
            f.write(res.content)
    else: None
    return fileName


def saveNumber(fileName, saveNumPath, splitPath):
    import os
    import shutil
    from sklearn.preprocessing import StandardScaler
    if os.path.exists(splitPath):
        shutil.rmtree(splitPath)
    os.mkdir(splitPath)
    # 清空資料夾
    now = int(time.mktime(datetime.now().timetuple()))

    pil_image = PIL.Image.open(saveNumPath + fileName).convert('RGB')
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

    for idx, (x, y, w, h) in enumerate(ary):
        plt.figure()
        roi = open_cv_image[y:y+h, x:x + w]
        thresh = roi.copy()
        plt.imshow(thresh)
        plt.savefig(splitPath + '{}_0{}.png'.format(now, idx), dpi=100)
    plt.close('all')


def predictPhone(splitPath):
    from sklearn.preprocessing import StandardScaler
    import os

    clf = joblib.load('./number/581photo.pkl')
    data = []
    basewidth = 150
    phone = ""

    for idx, img in enumerate(sorted(os.listdir(splitPath))):
        pil_image = PIL.Image.open(splitPath + '{}'.format(img)).convert('L')
        # 打開數字圖檔位置
        # wpercent = (basewidth / float(pil_image.size[0]))
        # hsize = int((float(pil_image.size[1]) * float(wpercent)))
        hsize = 100
        img = pil_image.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        # resize圖檔大小
        data.append([pixel for pixel in iter(img.getdata())])
        # 將數字array到array

    scaler = StandardScaler()
    scaler.fit(data)
    phoneScaled = scaler.transform(data)
    phoneArray = clf.predict(phoneScaled)
    for num in phoneArray:
        phone += str(num)

    return phone

def check_format(phone,splitPath):
    count = 5
    while count > 0:
        if phone[0] !="0" or phone[:2] !="09":
            predictPhone(splitPath)
            count -= 1
        else:break
    return phone

def main():
    global row
    sqlite3_path = "./581_original.sqlite3"
    saveNumPath = "./number/phone/"
    splitPath = "./number/split/"

    conn = sqlite3.connect(sqlite3_path)
    cur = conn.cursor()
    get_query = "Select * From rent_temp;"
    update_query = "UPDATE rent_temp SET newPhone = ? WHERE url= ?"
    for idx, row in enumerate(cur.execute(get_query).fetchall()):
        # if row[16] == "" or None:
        try:
            fileName = download_photo(idx, row[4], saveNumPath)
            saveNumber(fileName, saveNumPath, splitPath)
            phone = predictPhone(splitPath)
            phone = check_format(phone, splitPath)
            cur.execute(update_query, (phone, row[0]))
            conn.commit()
        except Exception:
            cur.execute(update_query, (row[4], row[0]))
            conn.commit()

        if idx % 200 == 0:
            print("目前已經計算出第{}份".format(idx))

    print("all phone number insert finished")

import cv2
import matplotlib.pyplot as plt
import sqlite3
import numpy
from PIL import Image
import PIL
import time
from requests.packages.urllib3.exceptions import LocationParseError
from datetime import datetime
from sklearn.externals import joblib


if __name__ == "__main__":
    main()