def calc(expr):
    '''
    >>> calc("12+4*3+")
    '15'
    >>> calc("123*+2-")
    '5'
    '''

    a=[] 
    for i in expr: 
        if i.isdigit(): 
            a.append(int(i))
        elif i!='' :
            b=int(a.pop())
            c=int(a.pop())
            if i=='*':
                a.append((b*c))
            elif i=='+':
                a.append((b+c))
            elif i=='-':
                a.append((c-b))
        
            
            
            

    return str(a[0])

print(calc("123*+2-"))
import doctest
doctest.testmod()

