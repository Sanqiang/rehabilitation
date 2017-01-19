from selenium.Data import LinkExtractor

if __name__ == "__main__":
    py = LinkExtractor("urls_news.txt")
    #py.extract()
    py.extractFromXMLForNews()