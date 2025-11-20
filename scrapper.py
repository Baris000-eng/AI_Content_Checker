from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import platform

def scrap_text(link):
    options = Options()

    if platform.system() == "Darwin": 
        options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    elif platform.system() == "Windows": 
        options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"

   
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    # Open the web page
    driver.get(link)

    
    WebDriverWait(driver, 20).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    # Extract ALL the visible text
    page_text = driver.find_element(By.TAG_NAME, "body").text

    driver.quit()

    return page_text
    
if __name__ == "__main__":
    text=scrap_text("https://www.tagesschau.de/")

    print(text)


