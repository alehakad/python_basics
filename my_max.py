a = int(input("1 число: \n"))
b = int(input("2 число: \n"))
def max(a,b):
    if a>=b:
        return a
    return b
print("Большее число : ",max(a,b))
