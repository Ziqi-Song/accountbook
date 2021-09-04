# -*- coding: UTF-8 -*-
"""
资金变动的记录：消费记录、收入记录
"""
import time
import json
import os

from deal_category import Category


def add_deal():
    """
    Add a deal record.
    :return:
    """
    _RECORD_PATH = './Records/'

    date = {'year': 0, 'month': 0, 'day': 0}
    categories = Category()
    amount = 0
    note = ""

    print("请输入消费信息：")

    input_date = input("日期(yyyy-mm-dd)：")
    date['year']  = input_date.split('-')[0]
    date['month'] = input_date.split('-')[1]
    date['day']   = input_date.split('-')[2]

    record_file_name = str(date['year']) + '_' + str(date['month']) + '.json'

    if os.path.isfile(_RECORD_PATH + record_file_name):
        month_deal_list = json.load(open(_RECORD_PATH + record_file_name, 'r'))
    else:
        month_deal_list = []

    print("\n目前可选的消费类别有：")
    categories.show_category()
    category_index = int(input("请选择消费类别："))

    amount = float(input("\n请输入消费金额："))

    note = input("\n请输入消费详情：")

    deal_id = date['year'] + date['month'] + str(len(month_deal_list) + 1)

    deal = {'date': date,
            'category': category_index,
            'amount': amount,
            'note': note,
            'id': deal_id}

    month_deal_list.append(deal)
    json.dump(month_deal_list, open(_RECORD_PATH + record_file_name, 'w'))

    print("\n已保存。\n")


def get_monthly_deal(year, month):
    """
    Print all deal records of a specific month.
    :param year:
    :param month:
    :return:
    """
    categories = Category()
    _RECORD_PATH = './Records/'
    record_file_name = str(year) + '_' + str(month) + '.json'
    month_deal_list = json.load(open(_RECORD_PATH + record_file_name, 'r'))
    deal_count = len(month_deal_list)
    print("{}年{}月共有{}笔交易.".format(year, month, deal_count))

    for day in range(1, 32):
        for deal in month_deal_list:
            if int(deal['date']['year']) == int(year) and \
               int(deal['date']['month']) == int(month) and \
               int(deal['date']['day']) == int(day):
                for category in categories.category_list:
                    if category['id'] == deal['category']:
                        category_name = category['Chinese name']
                        break
                print("日期：{}-{}-{}".format(deal['date']['year'], deal['date']['month'], deal['date']['day']))
                print("类别：{}".format(category_name))
                print("消费金额：{}".format(deal['amount']))
                print("详情：{}".format(deal['note']))


def get_daily_deal(year, month, day):
    """
    打印指定日期的所有资金变动记录
    :param year:
    :param month:
    :param day:
    :return:
    """
    categories = Category()
    _RECORD_PATH = './Records/'
    record_file_name = str(year) + '_' + str(month) + '.json'
    month_deal_list = json.load(open(_RECORD_PATH + record_file_name, 'r'))

    for deal in month_deal_list:
        if int(deal['date']['year']) == int(year) and \
           int(deal['date']['month']) == int(month) and \
           int(deal['date']['day']) == int(day):
            for category in categories.category_list:
                if category['id'] == deal['category']:
                    category_name = category['Chinese name']
                    break
            print("日期：{}-{}-{}".format(deal['date']['year'], deal['date']['month'], deal['date']['day']))
            print("类别：{}".format(category_name))
            print("消费金额：{}".format(deal['amount']))
            print("详情：{}".format(deal['note']))
