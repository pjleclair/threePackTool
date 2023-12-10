# Phillip LeClair
# CS 5001
# Final Project
# 12/10/2023
# TestDriver.py executes a series of tests to ensure functionality of the project


# import unittest to create the testing framework
import unittest

# import Driver to execute the webdriver
from threePack import Driver

# import DataService to send API requests to Google Sheets
from requestData import DataService

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
        self.assertTrue(len(data['values']) > 0, msg='Returned sheet is empty!')
    def test_driver(self):
        ''' test_driver tests whether the webdriver scrapes listings correctly & saves a valid screenshot
        Parameters: None
        Returns nothing
        '''
        driver = Driver()
        tenant = 'Raleigh Foot & Ankle'
        city_state = 'Raleigh, NC'
        specialty = 'Foot & Ankle'
        # title = 'Doctor' -- optional
        results = driver.drive(tenant, city_state, specialty)
        height, width = results['screenshot_size']
        driver.quit()
        # check to see if listing dimensions are valid:
        self.assertTrue(results['width'] > 0 and results['height'] > 0)
        # check to see if screenshot dimensions are valid:
        self.assertTrue(height > 0 and width > 0)


def main():
    ''' Main function executes the tests
    Parameters: None
    Returns nothing
    '''
    unittest.main(verbosity=3)


if __name__ == "__main__":
    main()
