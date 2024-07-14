from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import queue


def transportVicSearch(search):
    options = Options()
    options.headless = True
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    url = f'https://vic.transportsg.me/metro/tracker/consist?consist={search}'
    
    # Open the URL in the browser
    driver.get(url)
    
    try:
        # Use WebDriverWait for explicit wait
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="trip "]')))
        
        # Find all elements with class "trip"
        elements = driver.find_elements(By.XPATH, '//div[@class="trip "]')
        
        if elements:
            trip_texts = [element.text for element in elements]
            print(trip_texts)
            return trip_texts
        else:
            return ["Error: No trips found. Train may be invalid or not currently running."]
    except Exception as e:
        return [f'Error: {e}']
    finally:
        driver.quit()

def montagueDays(queue):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    url = f'https://howmanydayssincemontaguestreetbridgehasbeenhit.com'
    
    # Open the URL in the browser
    driver.get(url)
    
    try:
        # Wait for the page to load
        driver.implicitly_wait(5)
        
        # Find all elements with class
        elements = driver.find_element_by_class_name('jss25')
        
        if elements:
            days = elements.text
            print(days)
            queue.put(days)
        else:
            return("`Error: Number not found`")
    except Exception as e:
        return(f'Error: {e}')
    finally:
        driver.quit()