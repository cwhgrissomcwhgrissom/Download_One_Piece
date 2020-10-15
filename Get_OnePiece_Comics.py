import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import requests
import os
import time

def get_onepiece_comics():
    base_url = 'http://www.acg456.com'
    his = ['/HTML/OnePiece/']
    r = requests.get(base_url + his[-1])
    soup = BeautifulSoup(r.content,'lxml')
    soup = soup.find_all('a',{'href':re.compile('/HTML/OnePiece/+[0,9]')})

    # 控制讓Browser可以用不開起來
    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    browser = webdriver.Chrome(chrome_options=option)

    for num in soup:
        get_dir_name = num.text

        # 從get_dir_name內取得第幾集的數字
        #--------------------------------------------------------------------------
        a = get_dir_name
        print(a)
        a = list(get_dir_name)
        print(a)
        b = []
        for n in range(len(a)-1):
            b.append(a[n])
        print(b)
        dir_num = ('').join(b)
        print(dir_num)
        #--------------------------------------------------------------------------
        os.makedirs('./OnePiece/' + get_dir_name, exist_ok=True)
        episode_num_url = base_url + num.get('href')
        print(episode_num_url)
        browser.get(episode_num_url)
        select = Select(browser.find_element_by_tag_name("select"))
        total_page = select.options
        total_page = len(total_page)
        print('Start to download img~!!')
        for i in range(1,total_page+1):
            each_num = "%03d" % i
            IMAGE_URL = 'http://pic.acg456.com/Pic/OnlineComic1/OnePiece/'+ dir_num +'/' + str(each_num) + '.png'
            print(IMAGE_URL)
            time.sleep(30)
            r = requests.get(IMAGE_URL,stream=True)
            soup = BeautifulSoup(r.content, 'lxml')

            with open('./OnePiece/'+ get_dir_name +'/image_'+ str(each_num) +'.png', 'wb') as f:
                for chunk in r.iter_content(chunk_size=32):
                    f.write(chunk)
        print('Download finished~!!')
        #f.close()
#---------------------------------------------------------------------------------------------------


get_onepiece_comics()