from selenium import webdriver
import queue
import re
import json
import urllib
import json
from nltk.tokenize import sent_tokenize, word_tokenize

class LinkExtractor():
    def __init__(self, file):
        self.driver = webdriver.PhantomJS() #webdriver.Firefox("/Applications/Firefox.app/Contents/MacOS/firefox-bin")
        self.crawller_queue = queue.Queue()
        self.visited_checker = set()

        seed_url = "https://newsela.com"
        self.crawller_queue.put(seed_url)
        # self.visited_checker.add(seed_url)

        self.file_handler = open(file,"w+")

    def extract(self):

        while not self.crawller_queue.empty():
            try:
                cur_url = self.crawller_queue.get()
                self.driver.get(cur_url)
                self.visited_checker.add(cur_url)
                links = self.driver.find_elements_by_tag_name("a")
                for link in links:
                    url = link.get_attribute("href")
                    if url is not None and re.match("(http[s]?:\/\/)?newsela\.com\/articles\/[a-zA-Z\/-]+\d+\/", url) is not None:
                        print(url)
                        self.file_handler.write(url + "\n")
                    if url not in self.visited_checker:
                        self.visited_checker.add(url)
                        self.crawller_queue.put(url)
            except:
                print("error: ", cur_url)

        self.driver.close()

    def extractFromXMLForNews(self):
        url_pattern = "https://newsela.com/api/v2/search?languages=en&page={NUMBER}&page_size=100"
        for page_numnber in range(1, 36):
            print("start processing", str(page_numnber), "\n")
            batch = ""
            url = url_pattern.replace("{NUMBER}", str(page_numnber))
            req = urllib.request.Request(url)
            json_code =urllib.request.urlopen(req).read()
            obj = json.loads(json_code.decode("utf-8"))
            art_list = (obj["hits"])["hits"]
            for art in art_list:
                url = (art["_source"])["url"]
                category = (art["_source"])["category"]
                cdata = "\t".join([url, category])
                batch = "\n".join((batch, cdata))
                if len(batch) >= 10000:
                    self.file_handler.write(batch)
            self.file_handler.write(batch)

class TextExtractor():
    base_url = "https://newsela.com/"
    urls = []

    def __init__(self):
        path = "/home/sanqiang/data/drive/chromedriver" #"/Users/zhaosanqiang916/data/"
        self.driver = webdriver.Chrome(path)
        self.driver_temp = webdriver.Chrome(path)

        # self.driver = webdriver.PhantomJS()
        # self.driver_temp = webdriver.PhantomJS()

    def extractUrls(self):
        f = open("urls_news2.txt", "r")
        for line in f:
            items = line.split("\t")
            if len(items) != 2:
                print(line)
                continue
            self.urls.append((items[0], items[1]))

    def login(self):
        self.driver.get("https://newsela.com/")
        self.driver.find_element_by_class_name("signin").click()
        self.driver.find_element_by_name("username").send_keys("zhaosanqiang916@gmail.com")
        self.driver.find_element_by_name("password").send_keys("123456")
        self.driver.find_element_by_class_name("submit-button").click()

        self.driver_temp.get("https://newsela.com/")
        self.driver_temp.find_element_by_class_name("signin").click()
        self.driver_temp.find_element_by_name("username").send_keys("zhaosanqiang916@gmail.com")
        self.driver_temp.find_element_by_name("password").send_keys("123456")
        self.driver_temp.find_element_by_class_name("submit-button").click()


    def extract(self):
        output = {}
        for url, category in self.urls:
            if category not in output:
                output[category] = []

            cur_url = "".join((self.base_url, url))
            try:
                self.driver.get(cur_url)
                #self.driver.add_cookie({"name": "sessionid_v2", "value": "1t834igt3mgj8lxsqy4cffc7pfdmltjk","domain":".newsela.com"})
                #article = self.driver.find_element_by_id("Article").text()
            except:
                print(cur_url, "all level")
            level_links = self.driver.find_elements_by_class_name("level-set")
            obj = {}
            for level_link in level_links:
                try:
                    tag = level_link.get_attribute("innerText")
                    if tag[-1] == "L":
                        grade_level = int(tag[0: -1])
                    else:
                        grade_level = 99999
                    href = level_link.get_attribute("href")
                    self.driver_temp.get(href)
                    tag = level_link.get_attribute("innerHTML")
                    #self.driver_temp.add_cookie({"name": "sessionid_v2", "value": "1t834igt3mgj8lxsqy4cffc7pfdmltjk","domain":".newsela.com"})
                    article = self.driver_temp.find_element_by_id("Article").get_attribute("innerText")
                    # grade_level = self.driver_temp.find_element_by_class_name("grade_level").get_attribute("innerText")
                    obj[grade_level] = article
                    print(grade_level)
                    output[category].append(obj)
                except:
                    print(cur_url, grade_level)

        output = json.dumps(output)
        f = open("news3.txt", "w")
        f.write(output)
        f.close()