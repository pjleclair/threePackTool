# Phillip LeClair
# CS 5001
# Final Project
# 12/10/2023
# driver.py runs the webdriver and saves the relevant threePack in a .png file


# import os to get working directory for saving files
import os
# import date to append current date to screenshot filename
from datetime import date

# import selenium to run the webdriver, create webdriver options, and search page elements
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


# import Image & BytesIO to crop & save screenshot
from PIL import Image
from io import BytesIO

class Driver():
    ''' Driver class creates an object to execute threePack scraping
    Parameters: None
    Attributes: driver - WebDriver
    '''
    def __init__(self):
        ''' Init function creates the Driver object
        Parameters: self
        Attributes: driver - WebDriver
        '''
        # initialize headless chrome driver
        chrome_options = Options()
        # chrome_options.add_argument("--headless=new")
        chrome_options.add_argument('--disable-canvas-aa')
        chrome_options.add_argument('--disable-webgl')
        # chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(options=chrome_options) #options=chrome_options
        self.driver.set_window_size(1920,1080)
    
    def drive(self, tenant, city_state, specialty, title = 'Doctor'):
        ''' drive executes the search and screenshot functionality
        Parameters:
            - self
            - tenant: string
            - city_state: string
            - specialty: string
            - title: string (optional)
        Returns a dictionary with height, width, and screenshot_size keys
        '''
        self.driver.get('http://www.google.com')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'APjFqb')))
        search_box = self.driver.find_element(By.ID,'APjFqb')
        search_box.send_keys(f'best {specialty} {title} in {city_state}')
        search_box.submit()

        # find places header to anchor screenshot location
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'YzSd')))
        places = self.driver.find_element(By.CLASS_NAME, 'YzSd')

        # move the driver to the element
        scroll_script = "arguments[0].scrollIntoView();"
        self.driver.execute_script(scroll_script, places)
        self.driver.implicitly_wait(1)

        # iterate through top listings to determine size of screenshot
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'VkpGBb')))
        listings = self.driver.find_elements(By.CLASS_NAME, 'VkpGBb')
        
        height = 0
        width = 0
        for listing in listings:
            # print(f'Result: {listing.text}')
            # print(f'\tSize: {listing.size}')
            height += listing.size['height']
            if listing.size['width'] > width:
                width = listing.size['width']
        height = height + places.size["height"]

        # initialize screenshot
        screenshot = self.driver.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))

        # set crop values, crop screenshot
        # margin = 50
        # left = location['x'] - margin
        # top = location['y'] - margin / 2
        # right = location['x'] + width
        # bottom = location['y'] + height + margin / 2
        # screenshot = screenshot.crop((left,top,right,bottom))

        # set filepath using current working directory, create directory for tenant if not existing, save screenshot
        path = os.getcwd() + f'/images/{tenant}'
        today = str(date.today())
        img_path = f'{path}/3pack - {today}.png'
        if not os.path.exists(path):
            os.makedirs(path)
        screenshot.save(img_path)
        print(f'Saved threePack for {tenant}')
        return {'height': height, 'width': width, 'screenshot_size': screenshot.size}
    
    def quit(self):
        self.driver.quit()

def main():
    ''' Main function executes an example use of Driver
    Parameters: None
    Returns nothing
    '''
    driver = Driver()
    tenant = 'Raleigh Foot & Ankle'
    city_state = 'Raleigh, NC'
    specialty = 'Foot & Ankle'
    # title = 'Doctor' -- optional
    driver.drive(tenant, city_state, specialty)
    driver.quit()

if __name__ == '__main__':
    main()