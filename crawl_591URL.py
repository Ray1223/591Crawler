def write_to_csv(links, savePath):
    with open(savePath, 'a', encoding='utf-8') as fw:
        fw.write('\n'.join(links) + '\n')


def main():
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from bs4 import BeautifulSoup
    import random
    import lxml
    import time

    chrome_path = "/usr/local/bin/chromedriver"
    taipei_Xpath = '//*[@id="area-box-body"]/dl[1]/dd[1]'
    homePage = "https://rent.591.com.tw/new/?kind=0&region=1"
    savePath = "591_test.csv"

    web = webdriver.Chrome(chrome_path)
    web.get(homePage)
    web.find_element_by_xpath(taipei_Xpath).click()  # 選地點
    time.sleep(random.randint(1, 3))

    error = 0
    pageNo = 0

    #get totalPage
    soup = BeautifulSoup(web.page_source, 'lxml')
    totalPage = int(soup.select('.pageNum-form')[5].text)
    missPage  = []
    while pageNo < totalPage:
        try:
            web.find_element_by_tag_name('body').send_keys(Keys.END)
            soup = BeautifulSoup(web.page_source, 'lxml')
            links = [('https:' + link['href'].strip()) for link in soup.select("h3 > a")]
            write_to_csv(links, savePath)
            web.find_element_by_link_text('下一頁').click()
            pageNo += 1

        except Exception as e:
            print(e, "There is trouble for crawling.The pageNo is {}".format(pageNo))
            missPage.append(pageNo)
            error += 1

        if pageNo % 30 == 0:
            print("目前已經處理591網站第{}頁".format(pageNo))
        time.sleep(random.randint(1, 3))
    print("There are {} missing page".format(missPage))
    web.close()
    web.quit()  # 關閉整個瀏覽器

if __name__ == '__main__':
    main()
    print("591 website crawling finished!")
