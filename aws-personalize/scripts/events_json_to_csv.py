import pandas as pd
import json
import ast

f = open('test.txt', 'r')
df = pd.read_csv('../dataset/eventbrite.csv')

for line in f.readlines():
	d = ast.literal_eval(line)
	sdf = pd.json_normalize(d, sep='_')
	df = df.append(sdf)

print(df)
df.to_csv('eventbrite.csv', index=True)
