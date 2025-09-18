a=float(input('1 число').replace(',','.'))
b=float(input('2 число').replace(',','.'))
sum=(a+b)//0.01/100
avg=sum/2
print(f'sum={sum},avg={avg:.2f}')
