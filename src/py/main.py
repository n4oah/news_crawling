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
from selenium.common.exceptions import NoSuchElementException

'''
SITE_ID = 'naver'
SEED_ID = 'news'

CONTEXT = 'http://news.naver.com/'
SEED_URL = 'News'
'''

KEYWORD = set()
KEYWORD.add('ㄱㅂ')

START_DATE = datetime.datetime.now() - datetime.timedelta(weeks=1)
END_DATE = datetime.datetime.now()

START_URL = 'https://search.naver.com/search.naver?query='
END_URL = '&sm=tab_srt&sort=1&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so%3Add%2Cp' \
          '%3Aall%2Ca%3Aall&mynews=0&mson=0&refresh_start=0&related=0&where=news&' \
          'nso=so%3Ar%2Cp%3Afrom' + '20180301' + 'to' + '20180331' + '%2Ca%3Aall'

PREFIX = 'news.naver.com'


def news_crawling(keyword):
    global driver
    driver = webdriver.Chrome()

    encoding = urllib.parse.quote(keyword)
    url = START_URL + encoding + END_URL
    temp_url = url

    driver.get(url)

    news_dict = dict()
    news_list = list()
    news_comment_list = list()

    while True:
        links = [a.get_attribute('href') for a in driver.find_elements_by_xpath("//div[@class='news mynews section']"
                                                                                "/ul[@class='type01']/li/dl/dd/a")]

        for link in links:
            driver.get(link)
            if driver.current_url.find(PREFIX) == -1:
                continue

            news_wrapper = driver.find_element_by_xpath("//div[@id='wrap']")

            news_vo = News()
            news_vo.crawling_url = link
            news_vo.posting_id = urllib.parse.parse_qs(urllib.parse.urlparse(link).query)['aid'][0]
            news_body_crawling(news_wrapper, news_vo)

            news_comment_vo = NewsComment()
            news_comment_crawling(news_wrapper, news_comment_vo)

            news_list.append(news_vo)
            news_comment_list.append(news_comment_vo)

        driver.get(temp_url)

        try:
            temp_url = driver.find_element_by_xpath("//div[@id='main_pack']/div[@class='paging']//strong/following-sibling::a").get_attribute('href')
            driver.get(temp_url)
        except NoSuchElementException:
            break

    news_dict['news'] = news_list
    news_dict['comment'] = news_comment_list

    print(news_list)


def datetime_format(dates):
    temp = str(dates).split(' ')
    date = temp[0].split('-')
    time = temp[1].split(':')

    return datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]))


def image_parse_byte_code(image):
    with urllib.request.urlopen(image) as img:
        return io.BytesIO(img.read()).read()


def news_body_crawling(driver, news_vo):
    news_body = driver.find_element_by_xpath(".//*[@id='articleBodyContents']")
    news_face = driver.find_element_by_xpath(".//div[@id='spiLayer']//"
                                             "ul[@class='u_likeit_layer _faceLayer']")

    news_vo.title = driver.find_element_by_xpath(".//*[@id='articleTitle']").text
    news_vo.content = news_body.text
    news_vo.write_date = datetime_format(driver.find_element_by_xpath(".//div[@class='article_info']/"
                                                                      "div[@class='sponsor']/"
                                                                      "span[@class='t11']").text)
    news_vo.image_url = [i.get_attribute('src') for i in news_body.find_elements_by_xpath(".//img")]
    news_vo.image_file = [image_parse_byte_code(i) for i in news_vo.image_url]

    suffix = "span[@class='u_likeit_list_count _count']"
    news_vo.like_count = news_face.find_element_by_xpath(".//li[@class='u_likeit_list good']//" +
                                                         suffix).text
    news_vo.warm_count = news_face.find_element_by_xpath(".//li[@class='u_likeit_list warm']//" +
                                                         suffix).text
    news_vo.sad_count = news_face.find_element_by_xpath(".//li[@class='u_likeit_list sad']//" +
                                                        suffix).text
    news_vo.angry_count = news_face.find_element_by_xpath(".//li[@class='u_likeit_list angry']//" +
                                                          suffix).text
    news_vo.want_count = news_face.find_element_by_xpath(".//li[@class='u_likeit_list want']//" +
                                                         suffix).text


def news_comment_crawling(driver, news_comment_vo):
    pass


if __name__ == "__main__":
    print('크롤링을 시작합니다.')
    global e
    e = 3
    for keyword in KEYWORD:
        print('검색 키워드 : ', keyword)
        news_crawling(keyword)
