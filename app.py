# Phillip LeClair
# CS 5001
# Final Project
# 12/10/2023
# app.py runs the application using Driver & DataService


# import Driver and DataService to execute the application
from driver import Driver
from dataService import DataService

from time import sleep


def runApplication():
    ''' runApplication imports data from Google Sheets and runs the driver
    Parameters: None
    Returns nothing
    '''
    # MK: 1zNHLVX9V1TsckqhpzMWzkhDyLQ4bIDUmaJ6uKlTpJCM
    # Test: 1ZbTHgQc5p61oDLcAHoj2iAWcfgYXJJibnCFMo9boShI
    # initialize data service, spreadsheet_id, and fails
    spreadsheet_id='1zNHLVX9V1TsckqhpzMWzkhDyLQ4bIDUmaJ6uKlTpJCM'
    service = DataService(spreadsheet_id)
    fails = []

    # try to get data from Google Sheets, otherwise print error
    try:
        data = service.getData(range='Master Kate')
    except:
        print("Error fetching data!")
        return

    # if there is nothing in the sheet besides headers, print a message and stop
    if len(data['values']) <= 1:
        print('No new data in sheet!')
        return
    
    # clean data from MK
    driver_data = list()
    for row in data['values']:
        if len(row) > 1:
            status = row[2]
            if status == 'Implementing' or status == 'Live - In Trial' or status == 'Paying Client' or status =='Retired':
                #print(row[4].split(','))
                full_practice_names = row[4].split(',')
                city_state = full_practice_names[len(full_practice_names) - 2].strip() + ', ' + full_practice_names[len(full_practice_names) - 1]
                practice_name = row[4]
                specialty = row[3]
                driver_data.append([practice_name, city_state.strip(), specialty])
    # print(driver_data)
    # driver_data = data['values']
    
    # if there is data, initialize the driver and iterate through the client list, executing the driver each time
    # if the driver fails, print a message and append the client name to the fails list
    err_count = 0
    driver = Driver()
    for practice in driver_data:
        try:
            if err_count >= 3:
                driver.quit()
                driver = Driver()
                err_count = 0
            sleep(2)
            driver.drive(practice[0], practice[1], practice[2])
        except:
            print(f'Error creating threePack for {practice[0]}')
            fails.append(practice)
            err_count += 1

    print('Complete!')

    attempts = 0
    # if there are fails, print them to the user and retry
    while len(fails) > 0 and attempts < 3:
        print('ThreePack encountered errors in the following...')
        for fail in fails:
            print(f'\t- {fail}')
        print('Retrying...')
        driver.quit()
        driver = Driver()
        fails_data = fails.copy()
        fails.clear()
        for practice in fails_data:
            try:
                driver.drive(practice[0], f'{practice[1]}, {practice[2]}', practice[3])
            except:
                print(f'Error creating threePack for {practice[0]}')
                fails.append(practice)
        attempts += 1
    print('ThreePack encountered errors in the following...')
    for fail in fails:
        print(f'\t- {fail}')
    # after the script finishes, terminate the driver and clear the Google Sheet
    driver.quit()
    # service.clearSheet()

def main():
    ''' Main function runs the application
    Parameters: None
    Returns nothing
    '''
    runApplication()


if __name__ == '__main__':
    main()
