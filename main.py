import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

driver_path = os.getenv('CHROMEDRIVER_PATH')
if driver_path:
    driver = webdriver.Chrome(driver_path)
else:
    raise EnvironmentError("Please set the CHROMEDRIVER_PATH environment variable.")
try:
    driver.get('https://www.defense.gov/News/Contracts/')
    #SCRAPE SHIT HEERE




finally:
    driver.quit()