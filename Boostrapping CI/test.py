from os import path
from collections import Counter

import numpy as np
import pandas as pd


csv = pd.read_csv(path.join('Assets', 'sample_casen2017.csv'))
csv = csv[csv['sexo'] == 2]

def bs_median(n):
    for x in range(n):
        sample = csv.sample(len(csv), replace = True)
        median = sample['yautcor'].median()
        yield median
        
arr = np.fromiter(bs_median(5000), dtype= int, count=5000)

arr = arr.tolist()

arr = Counter(arr)

arr = {key: arr[key] for key in sorted(arr)}

for key in arr.keys():
    print(key)

