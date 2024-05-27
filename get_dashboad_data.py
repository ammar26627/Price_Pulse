from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GetDashboardData():
    website = "https://sso.gem.gov.in/ARXSSO/oauth/doLogin"
    options = webdriver.ChromeOptions()
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service= service, options= options)

    def __init__(self, restricted_brands) -> None:
        self.restricted_brands = restricted_brands
        self.table_data = {
                "Name" : [],
                "P_Id" : [],
                "Brand" : [],
                "Our_Price" : [],
                "Lowest_Price" : [],
                "Link" : []
                }
        self.extractData()
        

    def scrapeTableData(self, table_html) -> None:
        '''Takes HTML Table WebElement as parameter and scrapes the table data
        using bs4 and save it in table_data dictionary.'''

        soup = BeautifulSoup(table_html, 'html.parser')
        table_row = soup.find('tbody').find_all('tr')
        for index, tr in enumerate(table_row, start=1):
            td= tr.find_all('td')
            try:
                self.table_data['Name'].append(td[0].text)
            except Exception as e:
                self.table_data['Name'].append(None)
                print(f"Cannot append name at index{index} due to error:")
                print(e)
            try:
                self.table_data['P_Id'].append(td[1].text)
            except Exception as e:
                self.table_data['P_Id'].append(None)
                print(f"Cannot append P_Id at index{index} due to error:")
                print(e)
            try:
                self.table_data['Brand'].append(td[5].text)
            except Exception as e:
                self.table_data['Brand'].append(None)
                print(f"Cannot append Brand at index{index} due to error:")
                print(e)
            try:
                self.table_data['Our_Price'].append(td[8].text)
            except Exception as e:
                self.table_data['Our_Price'].append(None)
                print(f"Cannot append name at index{index} due to error:")
                print(e)
            try:
                self.table_data['Link'].append(td[0].find("a").get("href"))
            except Exception as e:
                self.table_data['Link'].append(None)
                print(f"Cannot append Link at index{index} due to error:")
                print(e)
            self.table_data['Lowest_Price'].append(None)

    def extractData(self) -> dict:
        '''Prompt login page of Gem for manual login.
        The program waits 1000 seconds until user navigates to cataloge page.
        It navigates all the pages in pagination to scrape data of all products.
        Returns a dictionary of product data'''

        self.driver.get(self.website)

        # Prompt login page for user to enter login information and wait till login credentials has been submitted. 
        WebDriverWait(self.driver, 1000).until(EC.staleness_of(WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//input[@id='loginid']")))))
        WebDriverWait(self.driver, 1000).until(EC.staleness_of( WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//input[@id='loginid1']")))))

        while True:
            # Wait until table element has been found
            table = WebDriverWait(self.driver, 1000).until(
                            EC.presence_of_element_located((By.XPATH, "//table[@class='index responsive']")))
            self.scrapeTableData(table) 
            try:
                next_page = WebDriverWait(self.driver, 10).until(
                                    EC.element_to_be_clickable((By.XPATH, "//li[@class='pagination-next ng-scope']//a[@class='ng-binding']")))
                self.driver.execute_script("arguments[0].click();", next_page)
            except:
                self.driver.quit()
                break
        
        return self.table_data
        


