import csv
import datetime
import re
from typing import *
import tqdm
from textblob import TextBlob

raw_file_path = "./movies.txt"
order_file_path = "./csvs/comments.csv"
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
    label = None

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
        state = 0
        col_num = 9
        row_data = [None] * col_num
        label_width = [len(lineParser.label) for lineParser in lineParsers]
        movie_txt_enumerator = enumerate(movie_txt)
        for line_offset, line in tqdm.tqdm(movie_txt_enumerator, total=7911684):
            if line == '\n':
                assert state == 8
                row_data[6], row_data[7] = TextBlob(row_data[6] + ' ' + row_data[7]).sentiment
                order_writer.writerow(row_data)
                row_data = [None] * col_num
                state = 0
            else:
                if line.startswith(lineParsers[state].label):
                    row_data[state] = line[label_width[state] :-1]
                    state += 1
                else:
                    row_data[state] += ' ' + line
