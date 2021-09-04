# -*- coding: UTF-8 -*-

import time

import deal_process
import deal_statistics


def main():
    # Obtain today's date
    year = time.strftime('%Y', time.localtime())
    month = int(time.strftime('%m', time.localtime()))
    day = int(time.strftime('%d', time.localtime()))

    print("您好，今天是{}年{}月{}日，欢迎使用My Account Book.".format(year, month, day))

    while True:
        print("\n目前可以使用的操作有：")
        print("1 - 增加一条消费记录")
        print("2 - 收支数据统计")
        print("0 - 退出")

        operation_idx = input("您要进行什么操作？")

        if operation_idx == "1":
            deal_process.add_deal()
        elif operation_idx == "2":
            deal_statistics.process()
        elif operation_idx == "0":
            print("谢谢使用！\n")
            break

    # deal_process.get_monthly_deal(year, month)
    # deal_process.get_daily_deal(year, month, day)


if __name__ == '__main__':
    main()