def y(x):
    return x*x+3
print(sum(y(x) for x in range(10,30,2)))
