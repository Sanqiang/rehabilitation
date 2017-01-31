from selenium_base.util.data import TextExtractor

if __name__ == '__main__':
    te = TextExtractor()
    te.login()
    te.extractUrls()
    te.extract()