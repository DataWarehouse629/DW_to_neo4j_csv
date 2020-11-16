import csv

import tqdm
raw_file_path = "./movies.txt"
user_file_path = "./csvs/user.csv"
reviews_file_path = "./csvs/reviews.csv"


with open(raw_file_path, 'r', encoding='ISO-8859-1') as raw_file:
    with open(user_file_path, 'w', encoding='utf-8', newline='') as user_file, \
            open(reviews_file_path, 'w', encoding='utf-8', newline='') as reviews_file:
        user_file.write('userId:ID,profileName:string\n')
        reviews_file.write(':START_ID(userId),:END_ID(productId)\n')
        user_writer = csv.writer(user_file, quoting=csv.QUOTE_ALL)
        reviews_writer = csv.writer(reviews_file, quoting=csv.QUOTE_ALL)

        k_label_product = 'product/productId: '
        k_label_user = 'review/userId: '
        k_label_name = 'review/profileName: '
        k_product_start = len(k_label_product)
        k_user_start = len(k_label_user)
        k_name_start = len(k_label_name)

        for line in tqdm.tqdm(raw_file):
            if (line.startswith('p')):
                product_id = line[k_product_start:-2]
                line = next(raw_file)
                user_id = line[k_user_start:-2]
                line = next(raw_file)
                try:
                    profile_name: str = line[k_name_start: -2].replace('\n', '')
                except Exception as e:
                    print(e)
                    print(line)
                user_writer.writerow((user_id, profile_name))
                reviews_writer.writerow((user_id, product_id))
                line = next(raw_file)
                while line != '\n':
                    line = next(raw_file)
