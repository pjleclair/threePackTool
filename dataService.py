# Phillip LeClair
# CS 5001
# Final Project
# 12/10/2023
# dataService.py interacts with Sheets API to fetch data to power the webdriver


# import Google oauth2 and googleapiclient to interact with Sheets API
from google.oauth2.service_account import Credentials
import googleapiclient.discovery

# import os to get current working directory for locating credentials file
import os

class DataService():
    ''' DataService class creates an object to interact with Google Sheets API
    Parameters: None
    Attributes: service - GoogleApiClient
    '''
    def __init__(self, spreadsheet_id):
        ''' Init creates a connection to Google Sheets using the credentials.json file
        Parameters: self
        Attributes: service - GoogleApiClient
        '''
        path = os.getcwd() + "\credentials.json"
        credentials = Credentials.from_service_account_file(
            path,
            scopes = ['https://www.googleapis.com/auth/spreadsheets']
        )
        self.service = googleapiclient.discovery.build('sheets','v4',credentials=credentials)
        self.spreadsheet_id = spreadsheet_id
    
    def getData(self, range = 'Sheet1'):
        ''' GetData fetches data from a spreadsheet
        Parameters: range - optional string
        Returns a dictionary with 'range', 'majorDimension', and 'values' keys
        '''
        request = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id,range=range)
        response = request.execute()
        return response
    
    def clearSheet(self):
        ''' ClearSheet empties the Google Sheet after the driver is ran
        Parameters: self
        Returns nothing
        '''
        requests = [{
            "updateCells": {
                "range": {
                "startRowIndex": 1
                },
                "fields": "*"
            }
        }]
        body = {"requests": requests}
        request = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id, body = body)
        request.execute()

def main():
    ''' Main function executes an example use of DataService
    Parameters: None
    Returns nothing
    '''
    service = DataService(spreadsheet_id='1ZbTHgQc5p61oDLcAHoj2iAWcfgYXJJibnCFMo9boShI')
    print(service.getData())

if __name__ == '__main__':
    main()