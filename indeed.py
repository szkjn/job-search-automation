import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

PATH = '/usr/bin/chromedriver'
driver = webdriver.Chrome(PATH)

def acceptCookies():
    try :
        cookie = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
        cookie.click()
    except:
        pass

def scrape(what, where, nbrOfPages = 1):
    
    jobs = []
    pages = nbrOfPages * 10
    
    for i in range(0, pages, 10):
        
        driver.get(f"https://fr.indeed.com/jobs?q={what}&l={where}&start=" + str(i))
        driver.maximize_window()
            
        try: 
            popup = driver.find_element(By.ID, 'popover-x')
            popup.click()
        except:
            pass

        acceptCookies()
        driver.implicitly_wait(3)
        
        # WIP
        # nbr_of_results = driver.find_element(By.ID, 'searchCountPages').text
        # nbr_of_results = nbr_of_results.strip('Page 1 de ').strip(' emplois')
        # print(nbr_of_results)

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
    df.to_csv(f'jobs_{what}_{where}.csv')

scrape('computer vision', 'france', 5)

