from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import urllib.request

http = input("알고 싶은 웹 사이트 주소를 입력하세요 >> ")
html = urllib.request.urlopen(http)
soup = BeautifulSoup(html, 'html.parser')


what = input("어떤 태그를 보고싶은지 입력하세요 >> ")

tag = soup.find_all(what)


for i in tag:
    print(i)

