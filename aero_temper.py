with open('1.txt','r') as file:
    tp = map(float,file.read().split('\n'))
    tp1 = [float(i) for i in tp]
print(tp1)
print(max(tp1),sum(tp1)/len(tp1),len(set(tp1)),sep="\n")
    
