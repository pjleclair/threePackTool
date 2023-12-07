from google.oauth2.service_account import Credentials
import googleapiclient.discovery
import os

class DataService():
    def __init__(self):
        path = os.getcwd() + "\credentials.json"
        credentials = Credentials.from_service_account_file(
            path,
            scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        self.service = googleapiclient.discovery.build('sheets','v4',credentials=credentials)
    
    def getData(self, spreadsheet_id, range = 'Sheet1'):
        request = self.service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,range=range)
        response = request.execute()
        return response

def main():
    service = DataService()
    service.getData(spreadsheet_id='1ZbTHgQc5p61oDLcAHoj2iAWcfgYXJJibnCFMo9boShI')

if __name__ == '__main__':
    main()