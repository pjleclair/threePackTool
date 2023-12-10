# Phillip LeClair
# CS 5001
# Final Project
# 12/10/2023
# app.py runs the application using Driver & DataService


# import Driver and DataService to execute the application
from driver import Driver
from dataService import DataService


def runApplication():
    ''' runApplication imports data from Google Sheets and runs the driver
    Parameters: None
    Returns nothing
    '''

    # initialize data service, spreadsheet_id, and fails
    spreadsheet_id='1ZbTHgQc5p61oDLcAHoj2iAWcfgYXJJibnCFMo9boShI'
    service = DataService(spreadsheet_id)
    fails = []

    # try to get data from Google Sheets, otherwise print error
    try:
        data = service.getData()
    except:
        print("Error fetching data!")
        return

    # if there is nothing in the sheet besides headers, print a message and stop
    if len(data['values']) <= 1:
        print('No new data in sheet!')
        return
    
    # if there is data, initialize the driver and iterate through the client list, executing the driver each time
    # if the driver fails, print a message and append the client name to the fails list
    driver = Driver()
    for practice in data['values'][1:]:
        try:
            driver.drive(practice[0], practice[1], practice[2])
        except:
            print(f'Error creating threePack for {practice[0]}')
            fails.append(practice[0])

    print('Complete!')

    # if there are fails, print them to the user
    if len(fails) > 0:
        print('ThreePack encountered errors in the following...')
        for fail in fails:
            print(f'\t- {fail}')
    # after the script finishes, terminate the driver and clear the Google Sheet
    driver.quit()
    service.clearSheet()

def main():
    ''' Main function runs the application
    Parameters: None
    Returns nothing
    '''
    runApplication()


if __name__ == '__main__':
    main()
