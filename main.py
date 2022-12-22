# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
# from lambda_function import fetchUpdates
import re


def escapp():
    hello = '\ ^ stack\.\ * / overflo\\w\$arr = 1'
    escapes = '\b\n\r\t\\'
    for c in escapes:
         hello = hello.replace(c, '')

    print(hello)

escapp()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
