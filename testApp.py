# Phillip LeClair
# CS 5001
# Final Project
# 12/10/2023
# testApp.py executes a series of tests to ensure functionality of the project


# import unittest to create the testing framework
import unittest

# import os to check file size
import os
from datetime import date
from os.path import getsize

# import Driver to execute the webdriver
from driver import Driver

# import DataService to send API requests to Google Sheets
from dataService import DataService

class TestDriver(unittest.TestCase):
    ''' TestDriver class creates a series of tests
    Parameters: unnittest.TestCase
    '''
    def test_data_service(self):
        ''' test_data_service tests whether Google Sheets API is returning data
        Parameters: None
        Returns nothing
        '''
        spreadsheet_id='1ZbTHgQc5p61oDLcAHoj2iAWcfgYXJJibnCFMo9boShI'
        service = DataService(spreadsheet_id)
        data = service.getData()
        # check to see if the sheet has data
        self.assertTrue(len(data['values']) > 0, msg='Returned sheet is empty!')
    def test_driver(self):
        ''' test_driver tests whether the webdriver scrapes listings correctly & saves a valid screenshot
        Parameters: None
        Returns nothing
        '''
        driver = Driver()

        tenant = 'Aspen Valley Hospital'
        city_state = 'Aspen, CO'
        specialty = 'Medical'
        # title = 'Doctor' -- optional
        results = driver.drive(tenant, city_state, specialty)

        path = os.getcwd() + f'/images/{tenant}'
        today = str(date.today())
        img_path = f'{path}/3pack - {today}.png'
        img_size = getsize(img_path) / 1000
        height, width = results['screenshot_size']
        driver.quit()
        # check to see if listing dimensions are valid:
        self.assertTrue(results['width'] > 0 and results['height'] > 0, msg='Listing dimensions are invalid')
        # check to see if screenshot dimensions are valid:
        self.assertTrue(height > 0 and width > 0, msg='Screenshot dimensions are invalid')
        # check to see if screenshot image size is valid (greater than 100kb):
        self.assertTrue(img_size > 10, msg='Screenshot file size is invalid (<10kb)!')


def main():
    ''' Main function executes the tests
    Parameters: None
    Returns nothing
    '''
    unittest.main(verbosity=3)


if __name__ == "__main__":
    main()
