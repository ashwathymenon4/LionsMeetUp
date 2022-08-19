import pandas as pd

users = pd.read_csv('../dataset/user_data_personalize.csv', index_col=0)
user_item = pd.read_csv('../dataset/user_item_personalize.csv', index_col=0)

print(users)
tags = list()
for index, row in users.iterrows():
	tags.append(user_item[user_item['USER_ID'] == row['USER_ID']].sample(1)['category'].tolist()[0])

users['categories'] = tags
print(users)
users.to_csv('../dataset/user_data_tags_personalize.csv', index = True)