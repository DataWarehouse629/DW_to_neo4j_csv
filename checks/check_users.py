import csv

with open('./csvs/users.csv', encoding='utf-8', newline='') as users_csv:
    reader = csv.reader(users_csv)
    d = {}
    for row in reader:
        userId, profileName = row
        if profileName == 'A Customer':
            continue
        value = d.get(profileName)
        if not value:
            d.setdefault(profileName, userId)
        else:
            if value != userId:
                print(f'{userId}, {value}, {profileName}')