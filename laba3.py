#!/usr/bin/env python
# coding: utf-8

from lxml import objectify, etree, html
import urllib
from urllib import request
from urllib.request import urlopen
import pandas as pd
from pymystem3 import Mystem
import re
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from threading import Thread

from time import sleep
import csv

main_url = 'https://ria.ru'

topics = ['tag_thematic_category_Turizm', 'location_Crimea', 'tag_thematic_category_Dorogi', 'location_United_Kingdom', 'auto',
          'politics', 'science', 'society', 'world', 'incidents']

def get_url_news(n, topics):
    urls = []
    for topic in topics:
        driver = webdriver.Chrome('chromedriver.exe')
        driver.get(main_url + '/' + topic)
        print(main_url + '/' + topic)
        sleep(0.5)
        elem = driver.find_element_by_class_name("list-date")
        elem.click()
        sleep(1)
        elem = driver.find_element_by_class_name("date-range__ranges")
        elem = elem.find_elements_by_tag_name("li")
        elem[3].click()
        sleep(1)

        for i in range(n):
            elem = driver.find_element_by_class_name("list-more")
            driver.execute_script("arguments[0].click();", elem)
            sleep(1)

        elems = driver.find_elements_by_class_name('list-item__content')
        
        for elem in tqdm_notebook(elems):
            urls.append(elem.get_attribute('href'))
        driver.close()
        sleep(2)
    return urls

def getTextFromURL(urls, dict_):
    driver = webdriver.Chrome('chromedriver.exe')
    for url in urls:
        try:
            driver.get(url)
            title = driver.find_element_by_class_name("article__title").text
            text = driver.find_element_by_class_name("article__text").text
            dict_.update({title:text})
        except:
            pass
    driver.close()
    return dict_	

urls = get_url_news(n=5500, topics=topics)

with open('urlsAll.txt', 'w') as f:
    for item in urls:
        f.write("%s\n" % item)

urlsAll = []

with open('urlsAll.txt') as f:
    lines = f.readlines()
    for line in lines:
        urlsAll.append(line.split('\n')[0])

dict_ = {}

thread1 = Thread(target=getTextFromURL, args=(urlsAll[0:int(len(urlsAll)/2)], dict_))
thread2 = Thread(target=getTextFromURL, args=(urlsAll[int(len(urlsAll)/2):len(urlsAll)], dict_))

thread1.start()
thread2.start()

thread1.join()
thread2.join()

fo = open('dict.txt', "w")
for k, v in dict_.items():
    fo.write(str(k) + '; '+ str(v) + '\n')
fo.close()