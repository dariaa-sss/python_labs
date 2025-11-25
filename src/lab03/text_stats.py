import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), "..", "lib"))

from text import normalize, top_n, tokenize, count_freq

inf = input("")
print(f"Всего слов: {len(tokenize(inf))}")
print(f"Уникальных слов: {len(count_freq((tokenize(inf))))}")
print("Топ-5:")
for world, count in top_n(count_freq((tokenize(inf))))[:5]:
    print(f"{world}: {count}")
