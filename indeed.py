import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime

PATH = '/usr/bin/chromedriver'
driver = webdriver.Chrome(PATH)
date = str(datetime.datetime.now().date())

def acceptCookies():
    try :
        cookie = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
        cookie.click()
    except:
        pass

def scrape(what, where, nbrOfPages = 1):
    
    jobs = []
    nbr_of_results = 0
    pages = nbrOfPages * 10
    print('pages to scrape:', nbrOfPages)
    
    for i in range(0, pages, 10):
        
        driver.get(f"https://fr.indeed.com/jobs?q={what}&l={where}&start=" + str(i))
        driver.maximize_window()
            
        try: 
            popup = driver.find_element(By.ID, 'popover-x')
            popup.click()
        except:
            pass

        acceptCookies()
        driver.implicitly_wait(1)
        
        # sets number of max pages to scrape according to number of results
        if nbr_of_results == 0:
            results = driver.find_element(By.ID, 'searchCountPages').text
            results = results.strip(' emplois')[10:]
            nbr_of_results = int(results)
            max_pages = nbr_of_results // 15
            print('total results:', nbr_of_results)
            print('max pages:', max_pages)
        
        # breaks loop if maximum page has been been reached
        if i > max_pages * 10:
            break

        try:
            results = driver.find_elements(By.CLASS_NAME, 'resultWithShelf')
            for result in results:
                title = result.find_element(By.CSS_SELECTOR, 'h2 > span').text
                company_name = result.find_element(By.CLASS_NAME, 'companyName').text
                location = result.find_element(By.CLASS_NAME, 'companyLocation').text
                description = result.find_element(By.CLASS_NAME, 'job-snippet').text
                posted_since = result.find_element(By.CLASS_NAME, 'date').text
                
                job = {
                    'title': title,
                    'company_name': company_name,
                    'location': location,
                    'description': description,
                    'posted_since': posted_since
                }
                
                jobs.append(job)
            
        finally:
            print(f'{str(len(jobs))} jobs have been scraped.')
    
    what = what.replace(' ', '_')
    df = pd.DataFrame(jobs)     
    df.to_csv(f'indeed_{date}_{what}_{where}.csv')

scrape('machine learning internship', 'france', 10)

