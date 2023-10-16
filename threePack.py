import time

from selenium import webdriver
from selenium.webdriver.common.by import By

def main():
    driver = webdriver.Chrome()
    driver.get('http://www.google.com')
    time.sleep(2)

    search_box = driver.find_element(By.ID,'APjFqb')
    search_box.send_keys('ChromeDriver')
    search_box.submit()
    time.sleep(2)

    driver.quit()

if __name__ == '__main__':
    main()