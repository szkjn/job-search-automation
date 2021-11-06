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
    search.clear()
    search.send_keys("computer vision")
    search.send_keys(Keys.RETURN)
finally:
    time.sleep(1)
    
data = {
    'title': [],
    'company': [],
    'location': [],
    'posted_date': [],
    'about': [],
    'job_description': [],
    'requirements': []
}

try:
    wait = WebDriverWait(driver, 10)
    main = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'kxIArb')))
    
    jobs = main.find_elements(By.TAG_NAME, "article")
    
    for job in jobs:
        
        company = job.find_element(By.CLASS_NAME, "ais-Highlight-nonHighlighted").text        
        location = job.find_element(By.CLASS_NAME, "dLvFyn").text
        posted_date = job.find_element(By.TAG_NAME, "time").get_attribute("datetime")
        header = job.find_element(By.TAG_NAME, "h3")
        title = header.text
        header.click()
        main = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'sc-12bzhsi-16')))
        
        contents = main.find_elements(By.CSS_SELECTOR, "h2 + div")
        about = contents[0].text
        description = contents[1].text
        requirements = contents[2].text
                
        data['title'].append(title)
        data['company'].append(company)
        data['location'].append(location)
        data['posted_date'].append(posted_date)
        data['about'].append(about)
        data['job_description'].append(description)
        data['requirements'].append(requirements)
        
        driver.back()
except:
    print('There has been an error during the process.')
    
finally:
    print(data)