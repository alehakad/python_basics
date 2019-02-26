s = 'У лукоморья 123 дуб зеленый 456'
print("Позиция 'я': ",s.find('я'),"Букв 'у':",s.count('у'),sep = '\n')
if not(s.isalpha()):
   print(s.upper(),'\n')
print('Длина:',len(s),sep = '\n')
if len(s) > 4 :
    print(s.lower(),'\n')
s = 'О'+s[1:]
print(s)
