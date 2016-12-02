from selenium import webdriver
import queue
import re
import json
import urllib

class LinkExtractor():

    def __init__(self):
        self.driver = webdriver.PhantomJS() #webdriver.Firefox("/Applications/Firefox.app/Contents/MacOS/firefox-bin")
        self.crawller_queue = queue.Queue()
        self.visited_checker = set()

        seed_url = "https://newsela.com"
        self.crawller_queue.put(seed_url)
        # self.visited_checker.add(seed_url)

        self.file_handler = open("urls.txt","w+")

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

    def extractFromXML(self):
        batch = ""
        #https://newsela.com/api/v2/search?category=health&page=7&page_size=20&story_type=news&story_type=editorial&tiles=true&type=header
        url = "https://newsela.com/api/v2/search?category=health&page=1&page_size=1000&story_type=news&story_type=editorial&tiles=true&type=header"
        req = urllib.request.Request(url)
        json_code =urllib.request.urlopen(req).read()
        print(json_code)
        art_list = json.loads(json_code.decode("utf-8"))
        for art in art_list:
            url = art["url"]
            batch = "\n".join((batch, url))
            if len(batch) >= 10000:
                self.file_handler.write(batch)
        self.file_handler.write(batch)


if __name__ == "__main__":
    py = LinkExtractor()
    #py.extract()
    py.extractFromXML()