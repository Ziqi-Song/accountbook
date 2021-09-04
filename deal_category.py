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
            {"id": 1, "Chinese name": ""},
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
        for idx, category in enumerate(self.category_list):
            if category['id'] == category_id:
                print("You are deleting ", category["Chinese name"])
                while True:
                    choice = input("Are you sure to delete this deal category? (y/n)")
                    if choice == 'y':
                        deleted_category = self.category_list.pop(idx)
                        json.dump(self.category_list, open('./Config/category.json', 'w'))
                        print("Category has been deleted: ", deleted_category)
                        break
                    elif choice == 'n':
                        break
                    else:
                        print("Wrong input. Please enter your choice with 'y' or 'n'.")
                break

    def add_category(self, category_Chinese_name):
        """
        Add a category in category.json.
        Note: new category id is one bigger than the last existed category.
        :param category_Chinese_name: Chinese_name of the category
        :return:
        """
        if len(self.category_list) == 0:
            new_category = {
                "id": 0,
                "Chinese name": category_Chinese_name,
            }
        else:
            new_category = {
                "id": self.category_list[-1]['id'] + 1,
                "Chinese name": category_Chinese_name,
            }
        print("You are adding a new category: ", new_category)
        while True:
            choice = input("Are you sure to add this deal category? (y/n)")
            if choice == 'y':
                self.category_list.append(new_category)
                json.dump(self.category_list, open('./Config/category.json', 'w'))
                print("New category has been saved: ", new_category)
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

    def get_categories(self):
        return self.category_list



if __name__ == "__main__":
    category_manager = Category()
    category_manager.add_category("吃饭")
    category_manager.add_category("购物")
    category_manager.add_category("娱乐")
    category_manager.add_category("交通&车辆")
    category_manager.add_category("家庭外出")
    category_manager.add_category("育儿")
    category_manager.add_category("工作")
    category_manager.add_category("人情往来")
    category_manager.add_category("水电煤气")
    category_manager.add_category("房产")