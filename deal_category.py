# -*- coding: UTF-8 -*-
"""
Process the category information in ./Config/category.json
"""
import json
import os


class Category:
    """
    Manage deal categories: add, delete, show
    """
    def __init__(self):
        """
        Initialization of class.
        category_list = [
            {"name": "", "id": 1, "Chinese name"： ""},
            ......
        ]
        Note: category id starts from 1, not 0.
        """
        if os.path.isfile('./Config/category.json'):
            self.category_list = json.load(open('./Config/category.json', 'r'))
        else:
            print("<Category.__init__> Error: Cannot find category.json.")

    def delete_category(self, category_id):
        """
        Delete a specified category from category.json
        :param category_id: id of the category to be deleted
        :return:
        """
        for idx, category_info in enumerate(self.category_list):
            if category_info['id'] == category_id:
                print("You are deleting ", category_info)
                while True:
                    choice = input("Are you sure to delete this deal category? (y/n)")
                    if choice == 'y':
                        deleted_category_info = self.category_list.pop(idx)
                        json.dump(self.category_list, open('./Config/category.json', 'w'))
                        print("This category has been deleted: ", deleted_category_info)
                        break
                    elif choice == 'n':
                        break
                    else:
                        print("Wrong input. Please enter your choice with 'y' or 'n'.")
                break

    def add_category(self, category_English_name, category_Chinese_name):
        """
        Add a category in category.json.
        Note: new category id is one bigger than the last existed category.
        :param category_English_name: English name of the category
        :param category_Chinese_name: Chinese_name of the category
        :return:
        """
        new_category_info = {
            "name": category_English_name,
            "id": self.category_list[-1]['id'] + 1,
            "Chinese name": category_Chinese_name
        }
        print("You are adding a new category: ", new_category_info)
        while True:
            choice = input("Are you sure to add this deal category? (y/n)")
            if choice == 'y':
                self.category_list.append(new_category_info)
                json.dump(self.category_list, open('./Config/category.json', 'w'))
                print("New category has been saved: ", new_category_info)
                break
            elif choice == 'n':
                break
            else:
                print("Wrong input. Please enter your choice with 'y' or 'n'.")

    def show_category(self):
        """
        Print category
        :return:
        """
        for _, category in enumerate(self.category_list):
            print("{}: {} {}".format(category['id'], category['name'], category['Chinese name']))
