from selenium import webdriver
import json


class TextExtractor():
    base_url = "https://newsela.com/"
    urls = []

    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.driver_temp = webdriver.PhantomJS()

    def extractUrls(self):
        f = open("urls.txt", "r")
        for line in f:
            self.urls.append(line)

    def extract(self):
        output = []
        for url in self.urls:
            cur_url = "".join((self.base_url, url))
            self.driver.get(cur_url)
            #article = self.driver.find_element_by_id("Article").text()
            level_links = self.driver.find_elements_by_class_name("level-set")
            print(len(level_links))
            obj = {}
            for level_link in level_links:
                tag = level_link.get_attribute("innerHTML")
                href = level_link.get_attribute("href")
                self.driver_temp.get(href)
                article = self.driver.find_element_by_id("Article").get_attribute("innerHTML")
                obj[tag] = article
            output.append(obj)

        output = json.dumps(output)
        f = open("article.txt", "w")
        f.write(output)
        f.close()



if __name__ == '__main__':
    te = TextExtractor()
    te.extractUrls()
    te.extract()