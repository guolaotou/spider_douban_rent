import requests
from bs4 import BeautifulSoup
import json

class Splider_douban():
    def __init__(self):
        self.url = "https://www.douban.com/group/279962/discussion?start="  # 后面加offset
        self.offset = 25
        self.enough_data = None

    def _get_html_by_url(self, offset):
        """
        通过指定url得到25条原始数据
        :return:
        """
        htmlData = requests.get(self.url+str(offset)).text
        soup = BeautifulSoup(htmlData, "lxml")
        raw25 = soup.find("table", attrs={"class": "olt"}).select("a")
        return raw25

    def get_enough_data(self, page_num=100):
        """
        循环调用_get_html_by_url，制造足够数据集
        :return:
        """
        print("1. get_enough_data ing")
        lt = []
        for i in range(page_num + 1):
            lt.extend(self._get_html_by_url(i * self.offset))
            print("进度： %d / %d" % (i, page_num))
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
        json_type = json.dumps(data)
        with open("res_data.txt", "w") as f:
            f.write(json_type)


if __name__ == "__main__":
    spider = Splider_douban()
    raw_data = spider.get_enough_data(page_num=100)
    data_processed = spider.get_url_title(raw_data)
    # print(data_processed)

    res = spider.get_data_by_loc(data_processed, loc="五道口")
    spider.save2file(res)
    print(res)