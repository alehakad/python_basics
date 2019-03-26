a = input()
b = input()
try:
    a1 = int(a)
    b1 = int(b)

    
    o = input("Operator: ")

    if o == "*":
       print(a1*b1)
    elif o == "-":
        print(a1-b1)
    elif o == "/":
        try:
            print(a1/b1)
        except ZeroDivisionError:
            print("division by zero")
    elif o == "+":
         print(a1+b1)
except ValueError:
     print("not that type")
