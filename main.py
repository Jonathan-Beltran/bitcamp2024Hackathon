import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


class WebsiteScraper:
    def __init__(self, url):
        self.url = url
        self.driver = None

    def get_driver(self):
        # Check if CHROMEDRIVER_PATH is set
        driver_path = os.getenv('CHROMEDRIVER_PATH')
        if not driver_path:
            raise EnvironmentError("Please set the CHROMEDRIVER_PATH environment variable.")

        # Set Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')  # Optional: run in headless mode
        chrome_options.add_argument('--no-sandbox')  # Required for certain environments

        # Initialize Chrome driver
        self.driver = webdriver.Chrome(options=chrome_options)
        return self.driver

    def navigate_to_url(self):
        """Navigates the driver to the target URL."""
        if not self.driver:
            self.get_driver()
        self.driver.get(self.url)


def main():
    target_url = "https://www.defense.gov/News/Contracts/"

    # Set the CHROMEDRIVER_PATH environment variable
    os.environ['CHROMEDRIVER_PATH'] = '/path/to/chromedriver'  # Replace with your ChromeDriver path

    scraper = WebsiteScraper(target_url)
    scraper.navigate_to_url()

    # Your data extraction and processing logic using the driver object goes here
    # For example:
    print(scraper.driver.page_source)

    scraper.driver.quit()


if __name__ == "__main__":
    main()


#Alex code
def read_file(filename):
    with open(filename) as file:
        lines = file.readlines()
    return lines

def make_table(lines):
    data = []
    for line in lines
        data.appen(line)

    df = pd.DataFrame(data)

    x = 
#Code Extraction Alexanders Code


