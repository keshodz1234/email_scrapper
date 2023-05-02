import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait



def Driver():

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.page_load_strategy = 'eager'
    
    driver = uc.Chrome(use_subprocess=True,version_main=112)
    driver.set_page_load_timeout(15)
    driver.implicitly_wait=10

    return driver

