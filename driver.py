from threePack import Driver
from requestData import DataService

def main():
    driver = Driver()
    service = DataService()
    spreadsheet_id='1ZbTHgQc5p61oDLcAHoj2iAWcfgYXJJibnCFMo9boShI'

    try:
        data = service.getData(spreadsheet_id)
    except:
        print("Error fetching data!")
        return

    if len(data['values']) <= 1:
        print('No new data in sheet!')
        return
    print(data['values'])
    for practice in data['values'][1:]:
        driver.drive(practice[0], practice[1], practice[2])

    print('Complete!')
    driver.quit()


if __name__ == '__main__':
    main()
