# Program 1: Simple Calculator

num1 = 20
num2 = 5
operators = ["+", "-", "*", "/"]

print("---- Simple Calculator ----")
for operator in operators:
    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    elif operator == "*":
        result = num1 * num2
    elif operator == "/":
        result = num1 / num2
    else:
        result = "Invalid operator"
    print(f"{num1} {operator} {num2} = {result}")

# Program 2: Area Calculation (Circle, Rectangle, Square, Triangle)
import math

# Circle
radius = 7
circle_area = math.pi * radius ** 2

# Rectangle
length = 10
width = 5
rectangle_area = length * width

# Square
side = 6
square_area = side ** 2

# Triangle
base = 8
height = 4
triangle_area = 0.5 * base * height

print("---- Area Calculation ----")
print(f"Area of Circle (radius = {radius}): {circle_area:.2f}")
print(f"Area of Rectangle (length = {length}, width = {width}): {rectangle_area}")
print(f"Area of Square (side = {side}): {square_area}")
print(f"Area of Triangle (base = {base}, height = {height}): {triangle_area}")
