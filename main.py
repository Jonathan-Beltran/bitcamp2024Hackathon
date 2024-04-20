import os
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

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

    def extract_information(self):
        """Extracts information from the webpage using BeautifulSoup."""
        if not self.driver:
            self.get_driver()
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find all <h3> elements
        h3_elements = soup.find_all('h3')

        # Print the text content of each <h3> element
        for h3 in h3_elements:
            print(h3.get_text())

    def close_driver(self):
        """Closes the web driver."""
        if self.driver:
            self.driver.quit()

def main():
    target_url = "https://www.defense.gov/News/Contracts/"

    # Set the CHROMEDRIVER_PATH environment variable
    os.environ['CHROMEDRIVER_PATH'] = '/path/to/chromedriver'  # Replace with your ChromeDriver path

    scraper = WebsiteScraper(target_url)
    scraper.extract_information()
    scraper.close_driver()

if __name__ == "__main__":
    main()

#Alex code
def read_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return lines

def make_table(lines):
    # data = []
    # for line in lines:
    #     data.append(line)
    words = lines.split()
    labeled_data = {
        'text': [words],
        'category': ['Federal Agency', 'Values', 'dates', 'company names', 'locations']
    }
    df = pd.DataFrame(labeled_data)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['text'])

    classifier = multinomialNB()
    classifier.fit(X, df['category'])

    predicted_categories = classifier.predict(X)

    result_df = pd.dataFrame({
        'word': df['text'].iloc[0],
        'predicted_category': predicted_categories
    })
    print(result_df)
