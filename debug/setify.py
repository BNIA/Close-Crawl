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


with open('test.json', 'w') as cases:
    dump(sorted(list(discreps)), cases)

df = read_csv("../data/2015/2015_test.csv")

mask = df['Case Number'].isin(list(discreps))
df = df[~mask]

df.to_csv("2015_test.csv", index=False)
