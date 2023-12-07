from threePack import Driver
from requestData import DataService

def main():
    service = DataService()
    spreadsheet_id='1ZbTHgQc5p61oDLcAHoj2iAWcfgYXJJibnCFMo9boShI'
    fails = []

    try:
        data = service.getData(spreadsheet_id)
    except:
        print("Error fetching data!")
        return

    if len(data['values']) <= 1:
        print('No new data in sheet!')
        return
    
    driver = Driver()
    for practice in data['values'][1:]:
        try:
            driver.drive(practice[0], practice[1], practice[2])
        except:
            print(f'Error creating threePack for {practice[0]}')
            fails.append(practice[0])

    print('Complete!')
    driver.quit()


if __name__ == '__main__':
    main()
