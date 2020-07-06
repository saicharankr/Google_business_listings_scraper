import pandas as pd 
from bs4 import BeautifulSoup as bs
import urllib
import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions
import csv
import time

url="https://www.google.co.in/maps/search/pgs+in+bangalore/@12.9335155,77.5421952,13z/data=!3m1!4b1"
options = Options()
options.add_argument("--headless") # Runs Chrome in headless mode.
options.add_argument("--lang=en")
options.add_argument('--no-sandbox') # Bypass OS security model
driver = webdriver.Chrome(chrome_options=options)

driver.get(url)

def collect_data(sent_data,file_name):
    with open(file_name, 'w', newline='') as csvfile:
        fieldnames = ['names', 'ratings','no_reviews','phone_numbers','addresses','details','descriptions','open_closin_time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for each in sent_data:
            try:
                name=each.find('h3',attrs={'class':'section-result-title'}).text.encode(encoding="utf-8",errors='ignore').decode('utf-8')
                rating=each.find('span',attrs={'class':'cards-rating-score'}).text.encode(encoding="utf-8",errors='ignore').decode('utf-8')
                no_review=each.find('span',attrs={'class':'section-result-num-ratings'}).text.encode(encoding="utf-8",errors='ignore').decode('utf-8')
                phone_number=each.find('span',attrs={'class':'section-result-info section-result-phone-number'}).text.encode(encoding="utf-8",errors='ignore').decode('utf-8')
                address=each.find('span',attrs={'class':'section-result-location'}).text.encode(encoding="utf-8",errors='ignore').decode('utf-8')
                details=each.find('div',attrs={'class':'section-result-details-container'}).text.encode(encoding="utf-8",errors='ignore').decode('utf-8')
                descriptions=each.find('div',attrs={'class':'section-result-descriptions'}).text.encode(encoding="utf-8",errors='ignore').decode('utf-8')
                open_closin_time=each.find('div',attrs={'class':'section-result-hours-phone-container'}).text.encode(encoding="utf-8",errors='ignore').decode('utf-8')
            except:
                pass
            try:
                writer.writerow({'names': name, 'ratings': rating,'no_reviews':no_review,'phone_numbers':phone_number,'addresses':address,'details':details,'descriptions':descriptions,'open_closin_time':open_closin_time})
            except:
                pass

def no_pages(n):
    files=[]
    for i in range(0,n):
        response=bs(driver.page_source,'html.parser')
        data=response.find_all('div' ,attrs={'class':'section-result-content'})
        file_name='D:/workbench/Webscraping/collection'+str([i])+'.csv'
        files.append('D:/workbench/Webscraping/collection'+str([i])+'.csv')
        collect_data(data,file_name)
        time.sleep(10)
        print("clicking next page")
        driver.find_element_by_xpath('//*[@id="n7lv7yjyC35__section-pagination-button-next"]').click()
        print("clicked")
        time.sleep(6)
    combined_csv=pd.concat((pd.read_csv(file,encoding='latin1') for file in files),ignore_index=True)
    combined_csv.to_csv('D:/workbench/Webscraping/final_collection.csv',index=False, encoding='utf-8-sig')

 no_pages(4):          