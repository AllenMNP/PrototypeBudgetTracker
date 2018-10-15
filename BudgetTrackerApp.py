import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import gspread
import datetime as dt
from oauth2client.service_account import ServiceAccountCredentials

BUDGET = 200

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('Budget Tracker-6839f4b5aae1.json', scope)

gc = gspread.authorize(credentials)


worksheet = gc.open('Budget Spreadsheet').sheet1

records = worksheet.get_all_records()

print(records)

def update_data():
    dates = []
    totals = []

    for r in records:
        dates.append(r['Date'])
        totals.append(r['Total'])


    x = [dt.datetime.strptime(d,'%m/%d/%Y').date() for d in dates]

    y = []
    for date in x:
        y.append(BUDGET)    

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.plot(x,totals,'k.')
    plt.plot(x,y,'r--')
    plt.gcf().autofmt_xdate()
    plt.show(block = False)
    plt.pause(0.001)


def show_range_graph(start, end):
    dates = []
    totals = []

    for r in range(start, end):
        dates.append(records[r]['Date'])
        totals.append(records[r]['Total'])
        
    x = [dt.datetime.strptime(d,'%m/%d/%Y').date() for d in dates]

    y = []
    for date in x:
        y.append(BUDGET)    

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.plot(x,totals,'k.')
    plt.plot(x,y,'r--')
    plt.gcf().autofmt_xdate()
    plt.show(block = False)
    plt.pause(0.001)
    

def range_data(d1, d2):
    start_found = False
    start_index = 0
    end_index = 0
    for x in range(0, len(records)):
        if(begin_range(d1, d2, records[x]['Date']) and end_range(d1, d2, records[x]['Date'])):
            if(not start_found):
                start_found = True
                start_index = x
        if(start_found and not (begin_range(d1, d2, records[x]['Date']) and end_range(d1, d2, records[x]['Date']))):
            end_found = True
            end_index = x
            break
    show_range_graph(start_index, end_index)
            

def new_data():
    print("Enter Date (Format: MM/DD/YYYY) or Leave Blank For Today")
    date = input()
    if(date == ""):
        date = dt.datetime.today().strftime('%m/%d/%Y')
    else:
        date = date_format_checker(date)
    print("Enter Amount")
    amount = input()
    print("Enter Reason")
    reason = input()
    print("Enter + or -")
    value = input()
    letter = ""
    if(value == "-"):
        if(len(records) == 0):
            total = 0 - float(amount)
            letter = "M"
        else:
            total = float(records[-1]['Total']) - float(amount)
            letter = "M"
    elif(value == "+"):
        if(len(records) == 0):
            total = 0 + float(amount)
            letter = "P"
        else:
            total = float(records[-1]['Total']) + float(amount)
            letter = "P"
    else:
        total = 0
        letter = ""
    worksheet.append_row([date, float(amount), reason, total, letter], value_input_option='USER_ENTERED')  


def delete_data():
    print("Enter Date (Format: MM/DD/YYYY) or Leave Blank For Today")
    date = input()
    if(date == ""):
        date = dt.datetime.today().strftime('%m/%d/%Y')
    else:
        date = date_format_checker(date)
    print("Enter Amount To Remove")
    amount = input()
    print("Enter Reason or Leave Blank")
    reason = input()

    find_first = False 
    
    if(reason == ""):
        find_first = True
        
    for index in range(0, len(records)):
        if(records[index]['Date'] == date):
            if(float(records[index]['Expense']) == float(amount) and find_first == False):
                if(records[index]['Reason'].lower() == reason.lower()):
                    worksheet.delete_row(index + 2)
                    break
            else:
                worksheet.delete_row(index + 2)
                break
    

def get_info():
    data_found = False
    print("Enter Date (Format: MM/DD/YYYY) or Leave Blank For Today")
    date = input()
    if(date == ""):
        date = dt.datetime.today().strftime('%m/%d/%Y')
    else:
        date = date_format_checker(date)
    print("Enter Amount For Information")
    amount = input()

    for index in range(0, len(records)):
        if(records[index]['Date'] == date):
            if(float(records[index]['Expense']) == float(amount)):
                data_found = True
                reason = records[index]['Reason']
                info_string ="Date Requested: " + date + "\nTransaction Made: " + amount + "\nReason For Transaction: " + reason
                print(info_string)
                
        if(data_found):
            break

    if(not data_found):
        print("NO INFORMATION FOUND FOR DATE " + date + " AND AMOUNT " + amount)


def range_info(d1, d2):
    start_found = False
    for x in records:
        if(begin_range(d1, d2, x['Date']) and end_range(d1, d2, x['Date'])):
            start_found = True 
            info_string ="Date Requested: " + x['Date'] + "\nTransaction Made: " + str(x['Expense']) + "\nReason For Transaction: " + x['Reason']
            print(info_string)
            print()


    if(not start_found):
        print("NO INFORMATION FOUND")
            
            
        

def begin_range(d1, d2, compare_date):
    start_date_split = d1.split("/")
    end_date_split = d2.split("/")
    compare_split = compare_date.split("/")

    if(int(compare_split[2]) >= int(start_date_split[2]) and int(compare_split[2]) <= int(end_date_split[2])):
        if(int(compare_split[0]) >= int(start_date_split[0]) and int(compare_split[0]) < 13):
            if(int(compare_split[1]) >= int(start_date_split[1]) and int(compare_split[1]) < 32):
                return True

    return False


def end_range(d1, d2, compare_date):
    start_date_split = d1.split("/")
    end_date_split = d2.split("/")
    compare_split = compare_date.split("/")

    if(int(compare_split[2]) >= int(start_date_split[2]) and int(compare_split[2]) <= int(end_date_split[2])):
        if(int(compare_split[0]) <= int(end_date_split[0]) and int(compare_split[0]) > 0):
            if(int(compare_split[1]) <= int(end_date_split[1]) and int(compare_split[1]) > 0):
                return True

    return False


def date_format_checker(d):
    if('0' in d[0]):
        return d[1:]
    else:
        return d

def get_range():
    while(True):
        print("Enter the first date")
        first_date = input()
        first_date = date_format_checker(first_date)
        print("Enter the second date")
        second_date = input()
        second_date = date_format_checker(second_date)

        if(check_valid_dates(first_date, second_date)):
            print("Enter I for range information or G for range graph")
            answer = input()
            if(answer == "I"):
                range_info(first_date, second_date)
                break
            elif(answer == "G"):
                plt.close()
                range_data(first_date, second_date)
                break
            else:
                print("INVALID COMMAND")
        else:
            print("One or both of the dates were invalid")

def check_valid_dates(d1, d2):
    start_date_split = records[0]['Date'].split("/")
    end_date_split = records[-1]['Date'].split("/")
    first_split = d1.split("/")
    second_split = d2.split("/")

    valid = False
    
    if(int(first_split[2]) >= int(start_date_split[2])):
        if(int(first_split[0]) >= int(start_date_split[0]) and int(first_split[0]) < 13):
            if(int(first_split[1]) >= int(start_date_split[1]) and int(first_split[1]) < 32):
                if(int(second_split[2]) <= int(end_date_split[2])):
                    if(int(second_split[0]) <= int(end_date_split[0]) and int(second_split[0]) > 0):
                        if(int(second_split[1]) <= int(end_date_split[1]) and int(second_split[1]) > 0):
                            valid = True

    return valid
                          

MENU ="""
ENTER   : Enter a new transaction made
DELETE  : Delete a previous transaction
UPDATE  : Updates the graph to show current values
CLOSE   : Close the shown graph
INFO    : Find info about certain transaction
RANGE   : Display range of information or range on graph
EXIT    : Closes the program
"""

while(True):
    print(MENU)
    action = input()
    if(action == "ENTER"):
        new_data()
        records = worksheet.get_all_records()
    elif(action == "DELETE"):
        delete_data()
        records = worksheet.get_all_records()
    elif(action == "UPDATE"):
        plt.close()
        update_data()
    elif(action == "CLOSE"):
        plt.close()
    elif(action == "INFO"):
        get_info()
    elif(action == "RANGE"):
        get_range()
    elif(action == "EXIT"):
        break
    else:
        print("INVALID COMMAND")

print("The program will now exit")
plt.show()
