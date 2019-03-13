import math
flist = [2,4,9,16,25]
nlist1 = []
for i in range(len(flist)):
   nlist1.append(flist[i]**0.5)
print(nlist1)   
nlist2 = list(map(math.sqrt,flist))
print(nlist2)
nlist3 = [i**0.5 for i in flist]
print(nlist3)
