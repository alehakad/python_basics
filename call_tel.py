c = int(input("Введите код города: \n"))
m = int(input("Длительность разговора: \n"))
print("Стоимость: ")
if c // 100 == 3 :
      if c%10 == 3 :
          print(m*15)
      else :
          print(m*18)
elif c%10 == 5 :
    print(m*11)
else :
    print(m*13)
            
              
              
