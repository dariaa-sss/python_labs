n=int(input(''))
tr=0
fl=0
for i in range(n):
    s=input('Имя Возраст Формат_участия ')
    if 'True' in s:
        tr+=1
    else:
        fl+=1
print(f'out:{tr} {fl}')