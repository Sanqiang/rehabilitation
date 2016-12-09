from selenium import webdriver
import json


class TextExtractor():
    base_url = "https://newsela.com/"
    urls = []

    def __init__(self):
        self.driver = webdriver.Chrome("/Users/zhaosanqiang916/data/chromedriver")
        self.driver_temp = webdriver.Chrome("/Users/zhaosanqiang916/data/chromedriver")

        # self.driver = webdriver.PhantomJS()
        # self.driver_temp = webdriver.PhantomJS()

    def extractUrls(self):
        f = open("urls_news.txt", "r")
        for line in f:
            self.urls.append(line)

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
        output = []
        for url in self.urls:
            cur_url = "".join((self.base_url, url))
            self.driver.get(cur_url)
            #self.driver.add_cookie({"name": "sessionid_v2", "value": "1t834igt3mgj8lxsqy4cffc7pfdmltjk","domain":".newsela.com"})
            #article = self.driver.find_element_by_id("Article").text()
            level_links = self.driver.find_elements_by_class_name("level-set")
            print(len(level_links))
            obj = {}
            for level_link in level_links:
                tag = level_link.get_attribute("innerHTML")
                href = level_link.get_attribute("href")
                self.driver_temp.get(href)
                #self.driver_temp.add_cookie({"name": "sessionid_v2", "value": "1t834igt3mgj8lxsqy4cffc7pfdmltjk","domain":".newsela.com"})
                article = self.driver_temp.find_element_by_id("Article").get_attribute("innerText")
                grade_level = self.driver_temp.find_element_by_class_name("grade_level").get_attribute("innerText")
                obj[grade_level] = article
                print(grade_level)
            output.append(obj)

        output = json.dumps(output)
        f = open("news.txt", "w")
        f.write(output)
        f.close()



if __name__ == '__main__':
    te = TextExtractor()
    te.login()
    te.extractUrls()
    te.extract()