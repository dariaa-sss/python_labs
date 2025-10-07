from  itertools import *
def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    if not nums:
        raise ValueError('ValueError')
    return (min(nums), max(nums))

def  unique_sorted(nums: list[float | int]) -> list[float | int]:
    return list(sorted(set(nums)))

def flatten(mat: list[list | tuple]) -> list:
    for i in mat:
        if type(i) == str:
            return print('TypeError')
        if len(i)==0:
            del(i)
    return list(chain(*mat))


print(min_max([1.5, 2, 2.0, -3.1]))
print(unique_sorted([1,4,1,1,-6,-6,0.8]))
print(flatten([[1,4,1,1],[-6,-6,0.8]]))