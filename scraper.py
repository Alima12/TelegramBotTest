from selenium import webdriver
import time
from bs4 import BeautifulSoup

class Scraper:
    sleep_time = 15
    def __init__(self):
        # browser = webdriver.Chrome(executable_path="driver/chromedriver.exe")
        browser = webdriver.Firefox(executable_path="driver/geckodriver.exe")
        time.sleep(2)

        browser.get("http://www.tsetmc.com/Loader.aspx?ParTree=151312")
        time.sleep(self.sleep_time)
        self.scrapper = browser
    
    def update_price(self)->list:
        soup = BeautifulSoup(self.scrapper.page_source, "html.parser")
        result = soup.select("#trade > div.objbox > table> tbody > tr")[1:10]
        indexer = 0
        records = []
        for r in result:
            _temp_record = {}
            res = r.find_all("td")
            _temp_record["Symbol"] = res[-1].text
            _temp_record["FullName"] = res[-2].text
            _temp_record["Type"] = indexer
            _temp_record["LastPrice"] = res[11].text
            _temp_record["ClosedPrice"] = res[8].text
            indexer+=1
            records.append(_temp_record)

        return records
    
    def get_overall(self)->dict:
        soup = BeautifulSoup(self.scrapper.page_source, "html.parser")
        text = soup.select("#FastView > span.s")[0].text
        _temp = text.split("-")[0:2]
        
        self.scrapper.close()

        return {
            "count": _temp[0],
            "percent": _temp[1] 
        }
 