# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import logging
import random
from datetime import datetime


class Splider_douban():
    def __init__(self, url="https://www.douban.com/group/279962/discussion?start="):
        self.url = url
        self.offset = 25
        self.enough_data = None

    def _get_html_by_url(self, offset):
        """
        通过指定url得到25条原始数据
        :return:
        """
        header = {"user-agent": "Mozilla/5.0"}
        htmlData = requests.get(self.url+str(offset), headers=header).text
        soup = BeautifulSoup(htmlData, "lxml")
        try:
            raw25 = soup.find("table", attrs={"class": "olt"}).select("a")
        except AttributeError as e:
            logging.error(e)
            return "error"

        return raw25

    def _get_html_by_url_selenium(self, offset):
        """
        同 _get_html_by_url, 用selenium模拟浏览器
        参考链接 https://www.cnblogs.com/sesshoumaru/p/python-selenium-webdriver.html
        :return:
        """
        # 设置chrome浏览器无界面模式
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        browser = webdriver.Chrome(chrome_options=chrome_options)

        browser.get(self.url + str(offset))
        for i in range(1, 5):
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(0.05)

        soup = BeautifulSoup(browser.page_source, "lxml")
        raw25 = soup.find("table", attrs={"class": "olt"}).select("a")
        return raw25

    def get_enough_data(self, page_num=100, page_begin=0):
        """
        循环调用_get_html_by_url，制造足够数据集
        page_begin int:
            可选
        :return:
        """
        print("1. get_enough_data ing...")
        lt = []
        for i in range(page_begin, page_begin + page_num + 1):
            temp = self._get_html_by_url(i * self.offset)
            if temp is "error":
                print("error, i - page_begin = :", i - page_begin)
                print("\n")
                break
            lt.extend(temp)
            # lt.extend(self._get_html_by_url_selenium(i * self.offset))
            print("\n进度： %d / %d" % (i - page_begin, page_num))

            # 防止封IP
            if (i - page_begin) == 0:
                continue
            elif (i - page_begin) % 1000 == 0:
                sleep_time = random.randrange(5, 10) * 100
                print("1000 sleep, sleep_time:", sleep_time)
                time.sleep(sleep_time)
            elif (i - page_begin) % 100 == 0:
                sleep_time = random.randrange(5, 10) * 10
                print("100 sleep, sleep_time:", sleep_time)
                time.sleep(sleep_time)
            elif (i - page_begin) % 20 == 0:
                sleep_time = random.randrange(5, 10) * 1
                print("20 sleep, sleep_time:", sleep_time)
                time.sleep(sleep_time)
            elif (i - page_begin) % 10 == 0:
                sleep_time = random.randrange(5, 10) * 0.5
                print("10 sleep, sleep_time:", sleep_time)
                time.sleep(sleep_time)
            elif (i - page_begin) % 5 == 0:
                sleep_time = random.randrange(5, 10) * 0.2
                print("5 sleep, sleep_time:", sleep_time)
                time.sleep(sleep_time)
            else:
                sleep_time = random.randrange(5, 10) * 0.1
                print("1 sleep, sleep_time:", sleep_time)
                time.sleep(sleep_time)

        self.enough_data = lt
        print("\n")
        return lt

    def get_url_title(self, raw_data):
        """
        处理数据，得到url和title
        :return:
        """
        print("2. get_url_title ing...\n")
        lt_url_title = []
        for _ in raw_data:
            lt_url_title.append({"url": _.get("href"), "title": _.get("title")})
        return lt_url_title

    def get_data_by_loc(self, data, loc="五道口"):
        """
        根据指定地点，筛选只具有该地点的数据
        :param data:
        :param loc:
        :return:
        """
        print("3. get_data_by_loc ing...\n")
        res = []
        for _ in data:
            title = _.get("title")
            if title is None:
                continue
            if loc in _.get("title"):
                res.append(_)
        return res

    def save2file(self, data):
        print("4. saving data ing...")
        json_type = json.dumps(data)
        label = datetime.now().strftime("20%y%m%d_%s")
        with open("res_data%s.txt" % label, "w") as f:
            f.write(json_type)
        print("5. end.")


if __name__ == "__main__":
    # spider = Splider_douban()
    # spider = Splider_douban(url="https://www.douban.com/group/625354/discussion?start=")# 后面加offset
    spider = Splider_douban(url="https://www.douban.com/group/beijingzufang/discussion?start=")# 后面加offset

    raw_data = spider.get_enough_data(page_num=400, page_begin=0)
    # raw_data = spider.get_enough_data(page_num=100)

    data_processed = spider.get_url_title(raw_data)

    res = spider.get_data_by_loc(data_processed, loc="五道口")
    spider.save2file(res)
    print(res)
    print(json.dumps(res))

