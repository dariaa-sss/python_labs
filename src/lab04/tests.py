import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
from io_txt_csv import read_text, write_csv
txt = read_text("/Users/dariella/Desktop/python_labs/data/lab04/test.txt")
print(txt)# должен вернуть строку
write_csv([("word","count"),("test",3)], "/Users/dariella/Desktop/python_labs/data/lab04/check.csv")  # создаст CSV