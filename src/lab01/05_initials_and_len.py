name = input("ФИО: ")
inc = ""
len_name = 0
name_list = []
for i in name.split():
    inc += (i)[0]
    name_list.append(i)
for i in name_list:
    len_name = len_name + len(i) + 1


print(f"Инициалы:{inc}")
print(f"Длина строки: {len_name-1}")
