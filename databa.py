import csv

current_Values = {
    'id': 'blah',
    'last_reading': '24',
    'current_reading': '35',
    'due_amount': '50'
}


def save_values(abc: dict) -> None:
    '''
    This function will save values to the database file 

    parameters = dict ['id': str, 'last_reading' : str , 'current_reading' : str , 'due_amount' : str]

    returns : nothing
    '''
    my_list = []
    my_data = []
    found = False
    with open('database.csv', mode='r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        my_data = list(csvreader)
        # print(my_data)

    for x in my_data:
        try:
            if x[0] == abc['id']:
                print('existing user')
                x[1] = abc['last_reading']
                x[2] = abc['current_reading']
                x[3] = abc['due_amount']
                # print(my_data)
                # if found an old entry update it
                found = True
                break
        except IndexError:
            pass

        # if not enter a new entry
    if not found:
        print('new user')
        my_list.append(abc['id'])
        my_list.append(abc['last_reading'])
        my_list.append(abc['current_reading'])
        my_list.append(abc['due_amount'])
        my_data.append(my_list)

    with open('database.csv', mode='w', newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        # print(my_data)
        csvwriter.writerows(my_data)


def get_values(abc: dict) -> dict:
    '''
    This function will get the values from the database file 

    parameters = dict ['id': str]

    returns : fully populated dictionary
    '''
    my_data = []
    found - False
    with open('database.csv', mode='r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        my_data = list(csvreader)

    for x in my_data:
        try:
            if x[0] == abc['id']:
                abc['last_reading'] = x[1]
                abc['current_reading'] = x[2]
                abc['due_amount'] = x[3]
                # print(my_data)
                # if found an old entry update it
                found = True
                break
        except IndexError:
            pass
    if not found:
        print('Non existent customer')
        abc['last_reading'] = 'NA'
        abc['current_reading'] = 'NA'
        abc['due_amount'] = 'NA'

    return abc


if __name__ == '__main__':
    # save_values(current_Values)
    print(get_values({'id': 'blah'}))
