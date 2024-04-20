import os
import spacy
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
        """Extracts information from the webpage and associated websites."""
        self.navigate_to_url()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
        page_source = self.driver.page_source

        # Print out the HTML content of the webpage
        print("Page Source:", page_source)

        soup = BeautifulSoup(page_source, 'html.parser')

        # Find the main content area where links are located
        main_content = soup.find('div', class_='container content')

        # Find all links within the main content area
        if main_content:
            links = main_content.find_all('a', href=True)

            # Iterate through each link
            for link in links:
                website_url = link['href']
                if website_url:
                    self.driver.get(website_url)
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'p')))
                    website_page_source = self.driver.page_source
                    website_soup = BeautifulSoup(website_page_source, 'html.parser')

                    # Extract information from the associated website
                    h1_elements = website_soup.find_all('h1')
                    for h1 in h1_elements:
                        print("h1:", h1.get_text())

                    date_elements = website_soup.find_all('span', class_='date')
                    for date in date_elements:
                        print("Date:", date.get_text())

                    p_elements = website_soup.find_all('p')
                    for p in p_elements:
                        print("Paragraph:", p.get_text())
        else:
            print("Main content area not found")

    def close_driver(self):
        """Closes the web driver."""
        if self.driver:
            self.driver.quit()

def read_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return lines


def make_table(lines):
    words = lines.split()
    categories = ['Federal Agency', 'Values', 'dates', 'company names', 'locations']

    # Flatten the labeled_data dictionary
    labeled_data = {
        'text': [],
        'category': []
    }
    for word in words:
        labeled_data['text'].append(word)
        labeled_data['category'].append(categories)  # All words are associated with all categories

    # Create DataFrame
    df = pd.DataFrame(labeled_data)

    categories_array = [category for sublist in df['category'] for category in sublist]

    vectorizer = TfidfVectorizer()
    x = vectorizer.fit_transform(df['text'])

    classifier = MultinomialNB()
    classifier.fit(x, categories_array)

    predicted_categories = classifier.predict(X)

    result_df = pd.dataFrame({
        'word': df['text'],
        'predicted_category': predicted_categories
    })
    print(result_df)

# Jonathans Code
def process_text_into_ents(filename):
    nlp = spacy.load("en_core_web_sm")
    ent_dict = {}
    with open(filename, 'r') as file:
        doc = nlp(file.read())
    for ent in doc.ents:
        ent_type = ent.label_
        if ent_type not in ent_dict:
            ent_dict[ent_type] = [ent.text]
        else:
            ent_dict[ent_type].append(ent.text)
    return ent_dict


def process_entsDict_into_lists(ent_dict):
    ent_lists = {ent_type: ent_texts for ent_type, ent_texts in ent_dict.items()}
    return ent_lists

def main():
    target_url = "https://www.defense.gov/News/Contracts/"

    # Set the CHROMEDRIVER_PATH environment variable
    os.environ['CHROMEDRIVER_PATH'] = '/path/to/chromedriver'  # Replace with your ChromeDriver path

    scraper = WebsiteScraper(target_url)
    scraper.extract_information()
    scraper.close_driver()

    filename = 'exampleDOD.txt'
    ent_dict = process_text_into_ents(filename)
    ent_lists = process_entsDict_into_lists(ent_dict)
    print("MY CODE!!!!!!!!")
    for ent_type, ent_texts in ent_lists.items():
        print(f"{ent_type}: {ent_texts}")



if __name__ == "__main__":
    main()

