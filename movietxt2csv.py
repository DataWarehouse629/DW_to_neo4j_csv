import csv
import datetime
import re
from dataclasses import dataclass, field
from typing import *
import tqdm
import time
import random
raw_file_path = "./movies.txt"
order_file_path = "./csvs/orders.csv"
review_user_file_path = "./csvs/review_user.csv"
'''

'''

labels = [
    'product/productId: ',
    'review/userId: ',
    'review/profileName: ',
    'review/helpfulness: ',
    'review/score: ',
    'review/time: ',
    'review/summary: ',
    'review/text: '
]

'''
product/productId: B00006HAXW
review/userId: A1RSDE90N6RSZF
review/profileName: Joseph M. Kotow
review/helpfulness: 9/9
review/score: 5.0
review/time: 1042502400
review/summary: Pittsburgh - Home of the OLDIES
review/text: I have all of the doo wop DVD's and this one is as good or better than the
1st ones. Remember once these performers are gone, we'll never get to see them again.
Rhino did an excellent job and if you like or love doo wop and Rock n Roll you'll LOVE
this DVD !!
'''
types = {
    'index': int,
    'asin': str,
    'userId': str,
    'profilename': str
}


class ColData:
    def after_handle(self, s: str):
        return s


class ProductId(ColData):
    label = 'product/productId: '
    pattern = re.compile('(B[A-Z0-9]{9})|([0-9]{9}[0-9X])')

    def after_handle(self, s: str):
        try:
            assert self.pattern.match(s)
        except AssertionError as e:
            print(s)
        return s

class UserId(ColData):
    label = 'review/userId: '
    pattern = re.compile('(A[A-Z0-9]{5,13})|#oc-.*')

    def after_handle(self, s: str):
        try:
            assert self.pattern.match(s)
        except AssertionError as e:
            print(s)
        return s


class ProfileName(ColData):
    label = 'review/profileName: '


class Helpfulness(ColData):
    label = 'review/helpfulness: '
    pattern = re.compile('[1-9][0-9]*|0')

    def after_handle(self, s: str):
        numerator, denominator = s.split('/')
        try:
            assert self.pattern.match(numerator)
            assert self.pattern.match(denominator)
        except AssertionError as e:
            print(s)

        return numerator, denominator


class Score(ColData):
    label = 'review/score: '
    pattern = re.compile('[0-9].[0-9]')

    def after_handle(self, s: str):
        assert self.pattern.match(s)
        return s


class Time(ColData):
    label = 'review/time: '

    def after_handle(self, s: str):
        int(s)
        return s


class Summary(ColData):
    label = 'review/summary: '


class Text(ColData):
    label = 'review/text: '


class Blank(ColData):
    label = '\n'


lineParsers: List[ColData] = [ProductId(), UserId(), ProfileName(), Helpfulness(), Score(), Time(), Summary(), Text(),
                              Blank()]

with open(raw_file_path, 'r', encoding='ISO-8859-1') as movie_txt:
    with open(order_file_path, 'w', encoding='utf-8', newline='') as order_file:
        order_writer = csv.writer(order_file, quoting=csv.QUOTE_ALL)
        index = 0
        tasks = tqdm.tqdm(total=7911684)
        state = 0
        row_data = []
        for line in movie_txt:

            if state == -7:
                if line != '\n':
                    current_line += '\n' + line
                    continue
                else:
                    res = lineParsers[state].after_handle(current_line)
                    row_data.append(res)
                    state = 0

                    product_id = row_data[0]
                    user_id = row_data[1]
                    user_username = row_data[2]
                    user_gender = ord(user_id[-1]) % 2
                    order_time_local = time.localtime(float(row_data[6]))
                    order_time = time.strftime("%Y-%m-%d", order_time_local)
                    order_id = index
                    order_number_choice = random.randint(0, 9)
                    if order_number_choice == 9:
                        order_number = 3
                    elif order_number_choice == 8 or order_number_choice == 7:
                        order_number = 2
                    else:
                        order_number = 1
                    order_writer.writerow((order_id, order_time, order_number,
                                          user_id, user_username, user_gender,
                                          product_id))
                    tasks.update()
                    row_data.clear()
                    index += 1
                    continue
            if state < 0:
                if not line.startswith(lineParsers[(-state) + 1].label):
                    current_line += '\n' + line
                    continue
                else:
                    res = lineParsers[-state].after_handle(current_line)
                    row_data.append(res)
                    state = (-state) + 1
            if state in (2, 6, 7):
                current_line = line[len(lineParsers[state].label): -1]
                state = -state
                continue
            else:
                current_line = line[len(lineParsers[state].label): -1]
                res = lineParsers[state].after_handle(current_line)
                if state == 3:
                    row_data += res
                else:
                    row_data.append(res)
                state = state + 1
                continue
