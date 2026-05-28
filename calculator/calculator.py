# Calculator with arithmetic (Bonus square root)

import math

def multiply(num1, num2):
    result = num1 * num2
    print("\033[1mResult:\033[0m", result)

def sqrt(root1):
    root_result = math.sqrt(root1)
    print("\033[1mResult:\033[0m", root_result)

def add(add1, add2):
    add_result = add1 + add2
    print("\033[1mResult:\033[0m", add_result)

def subtract(sub1, sub2):
    sub_result = sub1 - sub2
    print("\033[1mResult:\033[0m", sub_result)

def divide(div1, div2):
    div_result = div1 / div2
    print("\033[1mResult:\033[0m", div_result)

operation = input("What operation do you want to perform? (add / multiply / subtract / divide / root / exit): ").lower()
if operation == "root":
    variable10 = int(input("Square root of: "))
    sqrt(variable10)

if operation == "add":
    variable4 = int(input("Number to add: "))
    variable5 = int(input("Add by how much? "))
    add(variable4, variable5)

if operation == "subtract":
    variable6 = int(input("Number to subtract: "))
    variable7 = int(input("Subtract by how much? "))
    subtract(variable6, variable7)

if operation == "divide":
    variable8 = int(input("Number to divide: "))
    variable9 = int(input("Divide by how much? "))
    divide(variable8, variable9)

if operation == "exit":
    exit
