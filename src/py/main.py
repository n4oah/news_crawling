# 2018-04-07자 네이버 뉴스 키워드 검색 크롤링

import requests
from bs4 import BeautifulSoup
from newsVo import News, NewsComment
from newsDao import *
import datetime
import urllib.parse
import urllib.request
from selenium import webdriver
import datetime
import io

'''
SITE_ID = 'naver'
SEED_ID = 'news'

CONTEXT = 'http://news.naver.com/'
SEED_URL = 'News'
'''

KEYWORD = set()
KEYWORD.add('김정은')

START_DATE = datetime.datetime.now() - datetime.timedelta(weeks=1)
END_DATE = datetime.datetime.now()

START_URL = 'https://search.naver.com/search.naver?query='
END_URL = '&sm=tab_srt&sort=1&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so%3Add%2Cp' \
          '%3Aall%2Ca%3Aall&mynews=0&mson=0&refresh_start=0&related=0&where=news&' \
          'nso=so%3Ar%2Cp%3Afrom' + '20180301' + 'to' + '20180331' + '%2Ca%3Aall'


def news_crawling(keyword):
    global driver
    driver = webdriver.Chrome()

    encoding = urllib.parse.quote(keyword)
    url = START_URL + encoding + END_URL

    driver.get(url)

    news_dict = dict()
    news_list = list()
    news_comment_list = list()

    links = [a.get_attribute('href') for a in driver.find_elements_by_xpath("//div[@class='news mynews section']"
                                                                            "/ul[@class='type01']/li/dl/dd/a")]

    for link in links:
        driver.get(link)

        news_wrapper = driver.find_element_by_xpath("//div[@id='wrap']")
        news_body    = news_wrapper.find_element_by_xpath(".//*[@id='articleBodyContents']")

        news_vo = News()
        news_vo.title = news_wrapper.find_element_by_xpath(".//*[@id='articleTitle']").text
        news_vo.content = news_body.text

        news_vo.write_date = datetime_format(news_wrapper.find_element_by_xpath(".//div[@class='article_info']/"
                                                                                "div[@class='sponsor']/"
                                                                                "span[@class='t11']").text)
        news_vo.crawling_url = link
        news_vo.posting_id = urllib.parse.parse_qs(urllib.parse.urlparse(link).query)['aid'][0]

        news_vo.image_file = list()
        news_vo.image_file = [i.get_attribute('src') for i in news_body.find_elements_by_xpath(".//img")]
        print(len(news_vo.image_file))
        #print(news_vo.image_file)
        '''
        images = news_body.find_elements_by_xpath(".//img")

        news_vo.image_file = image_parse_byte_code(images[0].get_attribute('src'))
        '''

        '''
        print(news_vo.title)
        print('-' * 500)
        print(news_vo.content)
        print('-' * 500)
        print(news_vo.crawling_url)
        print('-' * 500)
        print(news_vo.posting_id)
        print('-' * 500)
        print(news_vo.write_date, type(news_vo.write_date))
        print('-' * 500)
        '''


        #driver.back()
        break

    news_dict['news'] = news_list
    news_dict['comment'] = news_comment_list


def datetime_format(dates):
    temp = str(dates).split(' ')
    date = temp[0].split('-')
    time = temp[1].split(':')

    return datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]))


def image_parse_byte_code(image):
    with urllib.request.urlopen(image) as img:
        return io.BytesIO(img.read()).read()


if __name__ == "__main__":
    print('크롤링을 시작합니다.')
    global e
    e = 3
    for keyword in KEYWORD:
        print('검색 키워드 : ', keyword)
        news_crawling(keyword)
