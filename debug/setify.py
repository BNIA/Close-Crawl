from json import dump
from time import sleep

from pandas import read_csv
from tqdm import trange

df = read_csv('case_nums.csv')

cols = list(df)

df = df.fillna('')

city, scraper = df[cols[0]], df[cols[1]]

discreps = set([])

for i, j in zip(city, scraper):
    if i and not j:
        discreps.add(i)


# print (discreps)

bounds = range(20)
bounds = list(discreps)
list_range = len(bounds)

case_range = trange(
    list_range, desc='Crawling', leave=True
)


# for case_num in case_range:

#     case = '{:04d}'.format(int(str(bounds[case_num])[-4:]))
#     sleep(1)
#     case_range.set_description("Crawling {}".format(case))

with open('test.json', 'w') as cases:
    dump(list(discreps), cases)