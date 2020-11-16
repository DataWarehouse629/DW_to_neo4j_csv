import csv

with open('csvs/titles.csv', 'w', encoding='utf-8', newline='') as title_csv:
    headers = ('productId:ID(Product-ID)','title:string')
    writer = csv.writer(title_csv, quoting =csv.QUOTE_ALL)
    writer.writerow(headers)
    with open('titles.txt', encoding='utf-8') as titles:
        for line in titles:
            line = line.replace('\n', '')
            productId=line[7:17]
            title = line[18:]
            writer.writerow((productId,title))

with open('csvs/not_found.csv', 'w', encoding='utf-8', newline='') as title_csv:
    headers = ('productId:ID(Product-ID)',)

    writer = csv.writer(title_csv, quoting =csv.QUOTE_ALL)
    writer.writerow(headers)
    with open('not_found.txt') as not_found:
        for line in not_found:
            productId = line[7:17]
            writer.writerow((productId,))
