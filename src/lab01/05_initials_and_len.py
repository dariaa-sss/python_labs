name=input("ФИО: ").strip()
inc=''
for i in name.split():
    inc+=(i)[0]

print(f'Инициалы:{inc}')
print(f'Длина строки: {len(name)}')