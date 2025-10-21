import sys
import os

from src.lib.text import top_n

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from io_txt_csv import read_text, write_csv, frequencies_from_text
from text import normalize, top_n,tokenize, count_freq

txt = read_text("/Users/dariella/Desktop/python_labs/data/lab04/test2.txt")
norm=normalize(txt)
token=tokenize(norm)
counts=count_freq(token)
top=top_n(counts)


write_csv( top, "/Users/dariella/Desktop/python_labs/data/lab04/check2.csv",header=("word", "count"))

print(f"Всего слов: {len(token)}")
print(f'Уникальных слов:{len(counts)}')
print('Топ-5:')
for world,count in top[:5]:
     print(f'{world}: {count}')