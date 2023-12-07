import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from PIL import Image
from io import BytesIO

class Driver():
    def __init__(self):
        #initialize headless chrome driver
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        # chrome_options.add_argument('--disable-canvas-aa')
        # chrome_options.add_argument('--disable-webgl')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(options=chrome_options) #options=chrome_options
    
    def drive(self, tenant, city_state, specialty, title = 'Doctor'):
        self.driver.get('http://www.google.com')

        search_box = self.driver.find_element(By.ID,'APjFqb')
        search_box.send_keys(f'best {specialty} {title} in {city_state}')
        search_box.submit()

        #find places header to anchor screenshot location
        places = self.driver.find_element(By.CLASS_NAME, 'YzSd')
        location = places.location

        #iterate through top listings to determine size of screenshot
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

        print(location)
        print(f'height: {height}')
        print(f'width: {width}')

        #initialize screenshot
        screenshot = self.driver.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))

        #set crop values, crop screenshot
        margin = 50
        left = location['x'] - margin
        top = location['y'] - margin / 2
        right = location['x'] + width
        bottom = location['y'] + height + margin / 2
        screenshot = screenshot.crop((left,top,right,bottom))

        #set filepath using current working directory, create directory for tenant if not existing, save screenshot
        path = os.getcwd() + f'/images/{tenant}'
        if not os.path.exists(path):
            os.makedirs(path)
        screenshot.save(f'{path}/3pack.png')
        print(f'Saved threePack for {tenant}')
    
    def quit(self):
        self.driver.quit()

def main():
    driver = Driver()
    tenant = 'Raleigh Foot & Ankle'
    city_state = 'Raleigh, NC'
    specialty = 'Foot & Ankle'
    # title = 'Doctor' -- optional
    driver.drive(tenant, city_state, specialty)
    driver.quit()

if __name__ == '__main__':
    main()