# -*- coding: UTF-8 -*-
"""
统计收支情况，生成统计表或统计图
"""
import os
import json
from deal_category import Category
import matplotlib.pyplot as plt


def process():
    """
    入口函数：选择不同的统计功能
    :return:
    """
    print("请问要统计什么数据?")
    print("1 - 年收支")
    print("2 - 月收支")
    print("3 - 日收支")
    print("4 - 月支出分布")

    operation_idx = input("请选择:")

    if operation_idx == "1":
        year_balance_hist()
    elif operation_idx == "2":
        month_balance_hist()
    elif operation_idx == "3":
        day_balance_hist()
    elif operation_idx == "4":
        month_cost_bar()


def year_balance_hist():
    start_year = int(input("请问从哪一年开始统计？"))
    end_year = int(input("请问统计到哪一年为止？"))

    for year in range(start_year, end_year+1):
        for month in range(1, 13):
            record_file_name = str(year) + '_' + str(month)
            if os.path.isfile('./Records/' + record_file_name + ".json"):
                pass
            else:
                print("{}无收支记录。".format(record_file_name))


def month_balance_hist():
    pass


def day_balance_hist():
    pass


def month_cost_bar():
    """
    统计指定月份各门类支出的pie chart
    :return:
    """
    year = str(input("请问统计哪一年?"))
    month = str(input("请问统计哪个月?"))

    record_file_name = str(year) + "_" + str(month) + ".json"
    if not os.path.isfile("./Records/" + record_file_name):
        print("Error: {} does not exist.".format(record_file_name))
        return

    category = Category()
    category_list = category.category_list

    # 统计每个category的支出总数
    cost_list = []
    for _ in range(len(category_list) - 1):  # 有一个category是income，不参加支出统计，因此这里减1
        cost_list.append(0)

    with open("./Records/" + record_file_name) as record_file_obj:
        deal_list = json.load(record_file_obj)
        for deal in deal_list:
            if category_list[deal['category']] == 'income':
                continue
            else:
                cost_list[int(deal['category']) - 1] += float(deal['amount'])  # 因为category的id是从1开始的，因此这里减1

    # 绘图
    plt.figure(figsize=(14, 6), dpi=80)
    # ax1绘制category legend
    ax1 = plt.subplot2grid((2, 4), (0, 0), rowspan=2, colspan=1)
    # category legend不包括income类
    category_legend = [str(category['id']) + " - " + category['name'] for category in category_list if category['name'] != 'income']
    # 从上到下绘制category legend的每一类注释
    for idx in range(len(category_legend)):
        ax1.text(0.0, 1.0 - (idx + 1.0) / len(category_legend), category_legend[idx])
    # 设置坐标轴
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.spines['top'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.set_xticks([])
    ax1.set_yticks([])

    # ax2绘制cost_list
    ax2 = plt.subplot2grid((2, 4), (0, 1), rowspan=2, colspan=3)
    # 获取每个category的id
    labels = [str(category['id']) for category in category_list if category['name'] != 'income']
    # 绘制cost_list
    b2 = ax2.bar(labels, cost_list, alpha=0.8, width=0.8, color='yellow', edgecolor='red', lw=3)
    # 在每个类别的柱顶部显示该类别的具体数字
    for b in b2:
        h = b.get_height()
        ax2.text(b.get_x() + b.get_width() / 2, h, '%.2f'%h, ha='center', va='bottom')
    # 设置坐标轴
    ax2.spines['bottom'].set_linewidth(5)
    ax2.spines['left'].set_linewidth(5)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.set_title('Monthly Cost')
    ax2.set_xlabel('Category id')
    ax2.set_ylabel('Cost')

    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    plt.savefig("./Statistics/" + str(year) + "_" + str(month) + "_cost.png")
