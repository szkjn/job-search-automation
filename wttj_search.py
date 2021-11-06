from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = '/usr/bin/chromedriver'
driver = webdriver.Chrome(PATH)

driver.get("https://www.welcometothejungle.com/fr/jobs?query=&page=1&aroundQuery=&refinementList%5Bcontract_type_names.fr%5D%5B%5D=Stage")
driver.maximize_window()

try:
    wait = WebDriverWait(driver, 10)
    search = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ais-SearchBox-input')))
    search.send_keys("computer vision")
    search.send_keys(Keys.RETURN)
finally:
    time.sleep(1)
    
try:
    wait = WebDriverWait(driver, 10)
    main = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'kxIArb')))
    
    jobs = main.find_elements(By.TAG_NAME, "article")
    for job in jobs:
        header = job.find_element(By.TAG_NAME, "h3")
        company = job.find_element(By.CLASS_NAME, "ais-Highlight-nonHighlighted")
        location = job.find_element(By.CLASS_NAME, "dLvFyn")
        date = job.find_element(By.TAG_NAME, "time")
        print(company.text)
        print(header.text)
        print(location.text)
        print(date.get_attribute("datetime"))
except:
    pass

    
# time.sleep(5)
# driver.quit()