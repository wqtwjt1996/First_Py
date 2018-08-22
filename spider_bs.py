# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib import request
import time, os, datetime

FILE_PATH = "C:/Users/hasee/Documents/url_spider/text_link/link_list.txt"
BASE_DOWNLOAD_URL = "wenshu.court.gov.cn"
BASE_DOWNLOAD_PATH = 'C:/Users/hasee/Documents/url_spider/'
BASE_PAGE_NUM = 17

def spider_bs():
    file_list = readfile()
    #start = datetime.datetime.now()
    for url_document in file_list:
    #for m in range(1):
        try:
            driver = webdriver.Edge()
            driver.get(url_document)
            #driver.get("http://wenshu.court.gov.cn/list/list/?sorttype=1&number=UTWC2ZWB&guid=9b6964bc-0eb1-56c100ab-97fbc503df10&conditions=searchWord+1++%E8%A1%8C%E6%94%BF%E6%A1%88%E4%BB%B6+%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E8%A1%8C%E6%94%BF%E6%A1%88%E4%BB%B6&conditions=searchWord+%E6%96%B0%E7%96%86%E7%BB%B4%E5%90%BE%E5%B0%94%E8%87%AA%E6%B2%BB%E5%8C%BA%E9%AB%98%E7%BA%A7%E4%BA%BA%E6%B0%91%E6%B3%95%E9%99%A2%E7%94%9F%E4%BA%A7%E5%BB%BA%E8%AE%BE%E5%85%B5%E5%9B%A2%E5%88%86%E9%99%A2+++%E6%B3%95%E9%99%A2%E5%9C%B0%E5%9F%9F:%E6%96%B0%E7%96%86%E7%BB%B4%E5%90%BE%E5%B0%94%E8%87%AA%E6%B2%BB%E5%8C%BA%E9%AB%98%E7%BA%A7%E4%BA%BA%E6%B0%91%E6%B3%95%E9%99%A2%E7%94%9F%E4%BA%A7%E5%BB%BA%E8%AE%BE%E5%85%B5%E5%9B%A2%E5%88%86%E9%99%A2")
            new_window = 'window.open("www.baidu.com")'
            driver.execute_script(new_window)
            handle = driver.window_handles
            driver.switch_to_window(handle[0])
            for i in range(BASE_PAGE_NUM):
                try:
                    # driver.find_element_by_id("17_button").click()
                    # driver.find_element_by_id("17_input_20").click()
                    element = WebDriverWait(driver, 100).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, 'dataItem')))
                    try:
                        #time.sleep(2)
                        sections = driver.find_elements_by_class_name('dataItem')
                    except:
                        #time.sleep(1)
                        driver.find_element_by_xpath(
                            "//a[contains(text(),'下一页')]").click()  # selenium的xpath用法，找到包含“下一页”的a标签去点击
                        continue
                    for section in sections:
                        #time.sleep(3)
                        section_title = section.find_element_by_class_name('wstitle')
                        section_title = section_title.text.strip()
                        section_url = str(section.find_element_by_tag_name('a').get_attribute('href'))
                        driver.switch_to_window(handle[1])
                        #time.sleep(1)
                        download(section_url.replace("contents?", "content?"), section_title, handle, driver)
                        #time.sleep(2)
                        driver.switch_to_window(handle[0])
                    if i < BASE_PAGE_NUM - 1:
                        #time.sleep(2)
                        driver.find_element_by_xpath(
                            "//a[contains(text(),'下一页')]").click()  # selenium的xpath用法，找到包含“下一页”的a标签去点击
                        time.sleep(2)
                    if EC.alert_is_present()(driver):
                        switch = driver.switch_to_alert()
                        switch.accept()
                finally:
                    pass
            driver.quit()
        finally:           pass
    #end = datetime.datetime.now()
    #print("一大轮结束！！\n总计用时：" + str(end - start))

def download(url, title, handle, driver):
    driver.get(url)
    try:
        element = WebDriverWait(driver, 100).until(EC.presence_of_all_elements_located((By.ID, 'Content')))
        section = driver.find_element_by_id('DivContent')
        file_str = BASE_DOWNLOAD_PATH + str(title) + '.txt'
        file = open(file_str, 'w', encoding='utf-8')
        file.write(title+'\n')
        file.write(section.text)
        file.close()
        print(title)
    finally:
        pass

def readfile():
    file_list = []
    try:
        file = open(FILE_PATH, "r")
    except:
        print("读取链接文件出错！")
        os._exit(-1)
    for line in file.readlines():
        file_list.append(line[:-1])
    return file_list

if __name__ == "__main__":
    spider_bs()