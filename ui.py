from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import time
import calendar
from deal_category import Category
import json


def getCurrentDate():
    year = int(time.strftime('%Y', time.localtime()))
    month = int(time.strftime('%m', time.localtime()))
    day = int(time.strftime('%d', time.localtime()))
    return year, month, day

year, month, day = getCurrentDate()
category_manager = Category()


#创建主窗口
root = Tk()
root.title("Account Book")
root.geometry("1280x720")
root.resizable(0, 0)

# 创建控件
# Button
def button_callback():
    record = {
        'date': {
            'year': int(combobox_year.get()),
            'month': int(combobox_month.get()),
            'day': int(combobox_day.get()),
        },
        'price': float(entry_price.get()),
        'deal_type': deal_type.get(),
        'category': listbox_category.get(listbox_category.curselection()),
        'note': text_note.get(1.0, "end"),
    }

    summary = f"日期：{record['date']['year']}-{record['date']['month']}-{record['date']['day']}\n"
    if record['deal_type'] == 1:
        summary += f"收入：{float(entry_price.get())}\n"
    elif record['deal_type'] == 2:
        summary += f"支出：{float(entry_price.get())}\n"
    summary += f"类别：{record['category']}\n"
    summary += f"备注：{record['note']}"

    choice = messagebox.askokcancel(message=summary)
    if choice == True:
        records = json.load(open("./data/record.json", "r"))
        records.append(record)
        json.dump(records, open("./data/record.json", "w"))
    else:
        pass

button = Button(master=root, text="保存", command=button_callback)
button.place(x=650, y=330, width=360, height=40)

# Canvas
# img = Image.open("/Users/songziqi/Downloads/IMG_9283.JPG")
# img_tk = ImageTk.PhotoImage(img)
# canvas = Canvas(master=root)
# canvas.create_image(0, 0, anchor=NW, image=img_tk)
# canvas.place(x=100, y=150, width=img.size[0], height=img.size[1])

# Label
# Label1 = Label(text=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
# Label1.place(x=100, y=200)
# def trickit():
#     currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#     Label1.config(text=currentTime)
#     root.update()
#     Label1.after(1000, trickit)
# Label1.after(1000, trickit)

# Labels
label_deal_type = Label(master=root, text="类型：")
label_deal_type.place(x=300, y=50)
label_date = Label(master=root, text="日期：")
label_date.place(x=300, y=100)
label_total_price = Label(master=root, text="总额：")
label_total_price.place(x=300, y=150)
label_category = Label(master=root, text="分类：")
label_category.place(x=300, y=200)
label_note = Label(master=root, text="备注：")
label_note.place(x=600, y=50)

# RadioButton
deal_type = IntVar(value=2)
radiobutton_income = Radiobutton(master=root, text="收入", variable=deal_type, value=1)
radiobutton_income.place(x=350, y=50)
radiobutton_outcome = Radiobutton(master=root, text="支出", variable=deal_type, value=2)
radiobutton_outcome.place(x=420, y=50)

# ComboBox
# Year ComboBox
years = []
for v in range(1987, 2087):
    years.append(str(v))
combobox_year = ttk.Combobox(master=root, width=5, state='readonly', values=years)
combobox_year.current(year - 1987)
def combobox_year_callback(*args):
    return int(combobox_year.get())
combobox_year.bind("<<ComboboxSelected>>", combobox_year_callback)
combobox_year.place(x=350, y=100)
# Month ComboBox
months = []
for v in range(1, 13):
    months.append(v)
combobox_month = ttk.Combobox(master=root, width=5, state='readonly', values=months)
combobox_month.current(month-1)
def combobox_month_callback(*args):
    selected_year = int(combobox_year.get())
    selected_month = int(combobox_month.get())
    days = []
    for v in range(1, calendar._monthlen(selected_year, selected_month) + 1):
        days.append(v)
    combobox_day.config(values=days)
    return selected_month
combobox_month.bind("<<ComboboxSelected>>", combobox_month_callback)
combobox_month.place(x=430, y=100)
# Day ComboBox
days = []
for v in range(1, calendar._monthlen(year, month)+1):
    days.append(v)
combobox_day = ttk.Combobox(master=root, width=5, state='readonly', values=days)
combobox_day.current(day-1)
def combobox_day_callback(*args):
    return int(combobox_day.get())
combobox_day.bind("<<ComboboxSelected>>", combobox_day_callback)
combobox_day.place(x=510, y=100)

# ListBox
category_dict = category_manager.get_categories()
categories = []
for v in category_dict:
    categories.append(v["Chinese name"])
strvar_iterms = StringVar(value=categories)
listbox_category = Listbox(master=root, height=len(categories), selectmode="single", listvariable=strvar_iterms)
listbox_category.place(x=350, y=200)
def listbox_category_callback(*args):
    return listbox_category.get(listbox_category.curselection())
listbox_category.bind("<<ListboxSelect>>", listbox_category_callback)

# Entry
entry_default_value = DoubleVar(value=0.0)
entry_price = Entry(master=root, width=20, textvariable=entry_default_value)
entry_price.place(x=350, y=150)

# Text
text_note = Text(master=root, width=50, height=20, bg="white smoke")
text_note.place(x=650, y=50)


# 进入消息循环
root.mainloop()