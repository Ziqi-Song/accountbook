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
        Initialization of class
        category_list = [
            {"name": "", "id": 1, "Chinese name"： “”},
            ......
        ]
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
        if category_id <= 0 or category_id > len(self.category_list):
            print("<Category.delete_category> Error: category_id should be in range ({}, {})".format(0, len(self.category_list)))
        else:
            del self.category_list[category_id - 1]
        json.dump(self.category_list, open('./Config/category.json', 'w'))
        self.category_list = json.load(open('./Config/category.json', 'r'))

    def add_category(self, category_English_name, category_Chinese_name):
        """
        Add a category
        :param category_English_name: English name of the category
        :param category_Chinese_name: Chinese_name of the category
        :return:
        """
        self.category_list.append({'id': len(self.category_list) + 1,
                                   'name': category_English_name,
                                   'Chinese name': category_Chinese_name})
        json.dump(self.category_list, open('./Config/category.json', 'w'))
        self.category_list = json.load(open('./Config/category.json', 'r'))

    def show_category(self):
        """
        Print category
        :return:
        """
        for _, category in enumerate(self.category_list):
            print("{}: {} {}".format(category['id'], category['name'], category['Chinese name']))
