from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import time

def getPID(station):
    # Set up the webdriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = f"https://transportvic.me/mockups/metro-lcd/{station.lower()}/*/platform"
    print(f"PID URL: {url}")
    # Load the webpage
    driver.get(url)

    time.sleep(1)

    S = lambda X: driver.execute_script("return document.body.parentNode.scroll" + X)
    driver.set_window_size(S("Width"), S("Height"))

    screenshot_path = "utils/pid/image.png"
    driver.save_screenshot(screenshot_path)

    image = Image.open(screenshot_path)
    image.show()

    driver.quit()


getPID('Flagstaff')