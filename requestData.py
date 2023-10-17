from google.oauth2.service_account import Credentials
import googleapiclient.discovery
import os

def main():
    path = os.getcwd() + "\credentials.json"
    credentials = Credentials.from_service_account_file(
        path,
        scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    )

    service = googleapiclient.discovery.build('sheets','v4',credentials=credentials)
    #id for new client list:
    spreadsheet_id = '1ZbTHgQc5p61oDLcAHoj2iAWcfgYXJJibnCFMo9boShI'
    range_ = 'Sheet1'
    request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,range=range_)
    response = request.execute()
    print(response)

if __name__ == '__main__':
    main()