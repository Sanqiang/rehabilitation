from selenium_base.util.data import LinkExtractor

if __name__ == "__main__":
    py = LinkExtractor("urls_news2.txt")
    #py.extract()
    py.extractFromXMLForNews()