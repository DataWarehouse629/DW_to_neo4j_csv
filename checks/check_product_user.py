import csv

with open('../csvs/review_user.csv', encoding='utf-8', newline='') as product_user_csv:
    reader = csv.reader(product_user_csv)
    d = {}
    for row in reader:
        productId, userId = row
        value:set = d.get(productId)
        if not value:
            d.setdefault(productId, {userId})
        else:
            if userId in value:
                print(f'{userId}, {productId}, {value}')
            else:
                value.add(userId)