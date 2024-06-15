from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import time

def getPID(station):
    # Set up the webdriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (without opening a browser window)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # URL of the webpage you want to capture
    url = f"https://transportvic.me/mockups/metro-lcd/{station.lower()}/*/platform"
    print(f"PID URL: {url}")
    # Load the webpage
    driver.get(url)

    # Wait for the page to load completely
    time.sleep(1)  # Wait for 1 second

    # Set the window size to ensure the entire page is captured
    S = lambda X: driver.execute_script("return document.body.parentNode.scroll" + X)
    driver.set_window_size(S("Width"), S("Height"))

    # Save a screenshot of the webpage
    screenshot_path = "utils/pid/image.png"
    driver.save_screenshot(screenshot_path)

    # Optionally, open and display the image
    image = Image.open(screenshot_path)
    image.show()

    # Close the browser
    driver.quit()


getPID('Flagstaff')