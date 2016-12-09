from selenium import webdriver
import queue
import re
import json
import urllib
from bs4 import BeautifulSoup


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
                batch = "\n".join((batch, url))
                if len(batch) >= 10000:
                    self.file_handler.write(batch)
            self.file_handler.write(batch)


if __name__ == "__main__":
    py = LinkExtractor("urls_news.txt")
    #py.extract()
    py.extractFromXMLForNews()