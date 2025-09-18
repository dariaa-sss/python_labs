name=input("ФИО: ")
inc=''
for i in name.split():
    inc+=(i)[0]

print(f'Инициалы:{inc}')
print(f'Длина строки: {len(name)}')