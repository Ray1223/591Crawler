import time
import sqlite3

sqlite3_path = "./581.sqlite3"
conn3 = sqlite3.connect(sqlite3_path)
cur3 = conn3.cursor()
get_query = "Select * From rent_temp;"
"""mysql connect"""

import pymysql

IP = 'localhost'
passwd = 'ray1223'
user = 'root'
db = 'rent'
conn = pymysql.connect(host=IP, port=3306, user=user, passwd=passwd, db=db, charset='utf8')
cur = conn.cursor()

for idx, row in enumerate(cur3.execute(get_query).fetchall()):
    count = 0
    traffic = ""
    #     print(len(row[14]))
    #     traffic = ','.join('?' * len(row[14]))
    insert_query = "INSERT INTO rent_temp(url,title,seller,identity,phone,price,type,floor,totfloor,square, address,city,area,style,traffic,soldout,newPhone,rentGroup) \
       VALUES ('%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' ,'%s', '%s' , '%s' , '%s'  )" % \
                   (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11],
                    row[12], row[13], traffic, row[15], row[16], row[17])

    try:
        cur.execute(insert_query)
        count += 1
        if count % 10 == 0:
            print("There is {}th data".format(count))
        time.sleep(1)
        conn.commit()
    except Exception as e:
        print("MySQL : ", e)
        conn.rollback()
conn.close()
conn3.close()