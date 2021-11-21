from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import time
import datetime
import calendar
from deal_category import Category
import json
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# from matplotlib.figure import Figure
import matplotlib.pyplot as plt
# plt.rcParams['font.sans-serif']=['SimHei']
# plt.rcParams['axes.unicode_minus']=False
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
from matplotlib import font_manager
import numpy as np
from tqdm import *


def getCurrentDate():
    year = int(time.strftime('%Y', time.localtime()))
    month = int(time.strftime('%m', time.localtime()))
    day = int(time.strftime('%d', time.localtime()))
    return year, month, day

def dateInPeriod(date, start, end):
    current_date = datetime.datetime.strptime(f"{date['year']}-{date['month']}-{date['day']}", "%Y-%m-%d")
    start_date = datetime.datetime.strptime(f"{start['year']}-{start['month']}-{start['day']}", "%Y-%m-%d")
    end_date = datetime.datetime.strptime(f"{end['year']}-{end['month']}-{end['day']}", "%Y-%m-%d")
    delta_current_start = current_date - start_date
    delta_end_current = end_date - current_date
    if delta_current_start.days >= 0 and delta_end_current.days >= 0:
        return TRUE
    else:
        return FALSE



year, month, day = getCurrentDate()
category_manager = Category()



#创建主窗口
root = Tk()
root.title("Records Analyzer")
root.geometry("1280x720")
root.resizable(0, 0)


#创建Labels
label_date_start = Label(master=root, text="开始日期：")
label_date_start.place(x=10, y=10)
label_date_end = Label(master=root, text="结束日期：")
label_date_end.place(x=350, y=10)
label_category = Label(master=root, text="分类：")
label_category.place(x=700, y=10)


# ComboBox
# Year ComboBox
years = []
for v in range(1987, 2087):
    years.append(str(v))

combobox_year_start = ttk.Combobox(master=root, width=5, state='readonly', values=years)
combobox_year_start.current(year - 1987)
def combobox_year_start_callback(*args):
    return int(combobox_year_start.get())
combobox_year_start.bind("<<ComboboxSelected>>", combobox_year_start_callback)
combobox_year_start.place(x=80, y=10)

combobox_year_end = ttk.Combobox(master=root, width=5, state='readonly', values=years)
combobox_year_end.current(year - 1987)
def combobox_year_end_callback(*args):
    return int(combobox_year_end.get())
combobox_year_end.bind("<<ComboboxSelected>>", combobox_year_end_callback)
combobox_year_end.place(x=420, y=10)
# Month ComboBox
months = []
for v in range(1, 13):
    months.append(v)

combobox_month_start = ttk.Combobox(master=root, width=5, state='readonly', values=months)
combobox_month_start.current(month-1)
def combobox_month_start_callback(*args):
    selected_year = int(combobox_year_start.get())
    selected_month = int(combobox_month_start.get())
    days = []
    for v in range(1, calendar._monthlen(selected_year, selected_month) + 1):
        days.append(v)
    combobox_day_start.config(values=days)
    return selected_month
combobox_month_start.bind("<<ComboboxSelected>>", combobox_month_start_callback)
combobox_month_start.place(x=160, y=10)

combobox_month_end = ttk.Combobox(master=root, width=5, state='readonly', values=months)
combobox_month_end.current(month-1)
def combobox_month_end_callback(*args):
    selected_year = int(combobox_year_end.get())
    selected_month = int(combobox_month_end.get())
    days = []
    for v in range(1, calendar._monthlen(selected_year, selected_month) + 1):
        days.append(v)
    combobox_day_end.config(values=days)
    return selected_month
combobox_month_end.bind("<<ComboboxSelected>>", combobox_month_end_callback)
combobox_month_end.place(x=500, y=10)
# Day ComboBox
days = []
for v in range(1, calendar._monthlen(year, month)+1):
    days.append(v)

combobox_day_start = ttk.Combobox(master=root, width=5, state='readonly', values=days)
combobox_day_start.current(day-1)
def combobox_day_start_callback(*args):
    return int(combobox_day_start.get())
combobox_day_start.bind("<<ComboboxSelected>>", combobox_day_start_callback)
combobox_day_start.place(x=240, y=10)

combobox_day_end = ttk.Combobox(master=root, width=5, state='readonly', values=days)
combobox_day_end.current(day-1)
def combobox_day_end_callback(*args):
    return int(combobox_day_end.get())
combobox_day_end.bind("<<ComboboxSelected>>", combobox_day_end_callback)
combobox_day_end.place(x=580, y=10)
# Category ComboBox
category_dict = category_manager.get_categories()
categories = []
for v in category_dict:
    categories.append(v["Chinese name"])
combobox_category = ttk.Combobox(master=root, width=5, state='readonly', values=categories)
combobox_category.current(0)
def combobox_category_callback(*args):
    return combobox_category.get()
combobox_category.bind("<<ComboboxSelected>>", combobox_category_callback)
combobox_category.place(x=750, y=10)


# Button
# 指定时间段内的各类别支出
def btn_callback_date_vs_cost():
    # 设置窗口大小
    params = {
        'figure.figsize': '10, 4'
    }
    plt.rcParams.update(params)
    # 按category统计
    records = json.load(open("./data/record.json", "r"))
    category_cost = {}
    for category in category_manager.category_list:
        category_cost[category["Chinese name"]] = 0
    for record in tqdm(records):
        record_date = {}
        record_date['year'] = record['date']['year']
        record_date['month'] = record['date']['month']
        record_date['day'] = record['date']['day']
        start_date = {}
        start_date['year'] = int(combobox_year_start.get())
        start_date['month'] = int(combobox_month_start.get())
        start_date['day'] = int(combobox_day_start.get())
        end_date = {}
        end_date['year'] = int(combobox_year_end.get())
        end_date['month'] = int(combobox_month_end.get())
        end_date['day'] = int(combobox_day_end.get())
        if dateInPeriod(record_date, start_date, end_date):
            category_cost[record["category"]] += record["price"]

    data = []
    labels = []
    for key in category_cost.keys():
        labels.append(key)
        data.append(category_cost[key])

    # 创建Canvas
    fig = plt.figure()
    subfig = plt.subplot(1, 1, 1)

    x = np.arange(0, 10, 1)
    y = category_cost.values()
    plt.bar(range(len(data)), data, width=0.5, align='center', tick_label=labels)
    plt.grid(linestyle="-", axis='y', alpha=0.4)
    for a, b in zip(labels, data):
        plt.text(labels.index(a), b-0.3, '%.2f'%b, ha='center', va='bottom', fontsize=10)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x=10, y=50)
btn_date_vs_cost = Button(master=root, text="日期VS支出", command=btn_callback_date_vs_cost)
btn_date_vs_cost.place(x=1100, y=30, width=120, height=30)

# 某一特定类别在每个月的支出
def btn_callback_month_vs_one_category():
    # 设置窗口大小
    params = {
        'figure.figsize': '10, 4'
    }
    plt.rcParams.update(params)
    # 按category统计
    records = json.load(open("./data/record.json", "r"))
    category_cost = {}
    for record in tqdm(records):
        record_date = {}
        record_date['year'] = record['date']['year']
        record_date['month'] = record['date']['month']
        record_date['day'] = record['date']['day']
        start_date = {}
        start_date['year'] = int(combobox_year_start.get())
        start_date['month'] = int(combobox_month_start.get())
        start_date['day'] = int(combobox_day_start.get())
        end_date = {}
        end_date['year'] = int(combobox_year_end.get())
        end_date['month'] = int(combobox_month_end.get())
        end_date['day'] = int(combobox_day_end.get())
        if dateInPeriod(record_date, start_date, end_date) and record["category"] == combobox_category.get():
            key = str(record_date['year'])+"-"+str(record_date['month'])
            if key not in category_cost.keys():
                category_cost[key] = 0
            else:
                category_cost[key] += record["price"]

    data = []
    labels = []
    for key in category_cost.keys():
        labels.append(key)
        data.append(category_cost[key])

    # 创建Canvas
    fig = plt.figure()
    subfig = plt.subplot(1, 1, 1)

    x = np.arange(0, 10, 1)
    y = category_cost.values()
    plt.bar(range(len(data)), data, width=0.5, align='center', tick_label=labels)
    plt.grid(linestyle="-", axis='y', alpha=0.4)
    for a, b in zip(labels, data):
        plt.text(labels.index(a), b-0.3, '%.2f'%b, ha='center', va='bottom', fontsize=10)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x=10, y=50)
btn_month_vs_one_category = Button(master=root, text="月份VS品类支出", command=btn_callback_month_vs_one_category)
btn_month_vs_one_category.place(x=1100, y=70, width=120, height=30)

# 每个月的总支出
def btn_callback_month_vs_cost():
    # 设置窗口大小
    params = {
        'figure.figsize': '10, 4'
    }
    plt.rcParams.update(params)
    # 按category统计
    records = json.load(open("./data/record.json", "r"))
    category_cost = {}
    for record in tqdm(records):
        record_date = {}
        record_date['year'] = record['date']['year']
        record_date['month'] = record['date']['month']
        record_date['day'] = record['date']['day']
        start_date = {}
        start_date['year'] = int(combobox_year_start.get())
        start_date['month'] = int(combobox_month_start.get())
        start_date['day'] = int(combobox_day_start.get())
        end_date = {}
        end_date['year'] = int(combobox_year_end.get())
        end_date['month'] = int(combobox_month_end.get())
        end_date['day'] = int(combobox_day_end.get())
        if dateInPeriod(record_date, start_date, end_date):
            key = str(record_date['year'])+"-"+str(record_date['month'])
            if key not in category_cost.keys():
                category_cost[key] = 0
            else:
                category_cost[key] += record["price"]

    data = []
    labels = []
    for key in category_cost.keys():
        labels.append(key)
        data.append(category_cost[key])

    # 创建Canvas
    fig = plt.figure()
    subfig = plt.subplot(1, 1, 1)

    x = np.arange(0, 10, 1)
    y = category_cost.values()
    plt.bar(range(len(data)), data, width=0.5, align='center', tick_label=labels)
    plt.grid(linestyle="-", axis='y', alpha=0.4)
    for a, b in zip(labels, data):
        plt.text(labels.index(a), b - 0.3, '%.2f' % b, ha='center', va='bottom', fontsize=10)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x=10, y=50)
btn_month_vs_cost = Button(master=root, text="月份VS总支出", command=btn_callback_month_vs_cost)
btn_month_vs_cost.place(x=1100, y=110, width=120, height=30)


# 进入消息循环
root.mainloop()





# import tkinter
# import numpy as np
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# from matplotlib.backend_bases import key_press_handler
# from matplotlib.figure import Figure
#
# root = tkinter.Tk()  # 创建tkinter的主窗口
# root.title("在tkinter中使用matplotlib")
#
# f = Figure(figsize=(5, 4), dpi=100)
# a = f.add_subplot(111)  # 添加子图:1行1列第1个
#
# # 生成用于绘sin图的数据
# x = np.arange(0, 3, 0.01)
# y = np.sin(2 * np.pi * x)
#
# # 在前面得到的子图上绘图
# a.plot(x, y)
#
# # 将绘制的图形显示到tkinter:创建属于root的canvas画布,并将图f置于画布上
# canvas = FigureCanvasTkAgg(f, master=root)
# canvas.draw()  # 注意show方法已经过时了,这里改用draw
# canvas.get_tk_widget().pack(side=tkinter.TOP,  # 上对齐
#                             fill=tkinter.BOTH,  # 填充方式
#                             expand=tkinter.YES)  # 随窗口大小调整而调整
#
# # matplotlib的导航工具栏显示上来(默认是不会显示它的)
# toolbar = NavigationToolbar2Tk(canvas, root)
# toolbar.update()
# canvas._tkcanvas.pack(side=tkinter.TOP,  # get_tk_widget()得到的就是_tkcanvas
#                       fill=tkinter.BOTH,
#                       expand=tkinter.YES)
#
#
# def on_key_event(event):
#     """键盘事件处理"""
#     print("你按了%s" % event.key)
#     key_press_handler(event, canvas, toolbar)
#
#
# # 绑定上面定义的键盘事件处理函数
# canvas.mpl_connect('key_press_event', on_key_event)
#
#
# def _quit():
#     """点击退出按钮时调用这个函数"""
#     root.quit()  # 结束主循环
#     root.destroy()  # 销毁窗口
#
#
# # 创建一个按钮,并把上面那个函数绑定过来
# button = tkinter.Button(master=root, text="退出", command=_quit)
# # 按钮放在下边
# button.pack(side=tkinter.BOTTOM)
#
# # 主循环
# root.mainloop()
