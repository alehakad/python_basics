import random 
l = ['самовар','весна','лето'] 
sl = random.choice(l) 
pos = random.randint(0,len(sl)-1) 
bv = sl[pos] 
print(sl[:pos]+'?'+sl[(pos+1):]) 
a = input("Угадайте букву\n") 
if a==bv: 
    print('победа\n') 
else: 
    print("не та\n") 
print("слово: ",sl)
