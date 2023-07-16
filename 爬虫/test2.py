import pandas
import numpy


df = pandas.read_csv('./all_movies2.csv')
print(df.shape)
# 去重
df.drop_duplicates(subset=['title','detail_url'],ignore_index=True,inplace=True)
print(df.shape)

# 删除所有为空的数据
# df2 = df.dropna()
# print(df2.shape)

# 删除rate为空的数据
index_list = df.loc[df['rate'].isnull()].index
df.drop(index=index_list, inplace=True)
print(df.shape)

# 删除真人秀节目
drop_index = df.loc[df['types'].str.contains('真人秀', na=False)].index
df.drop(index=drop_index, inplace=True)
print(df.shape)

df.reset_index(drop=True, inplace=True)
df['id'] = [i+1 for i in df.index.tolist()]
df.set_index('id', inplace=True)
print(df)

df.drop(columns='comments', inplace=True)
print(df)
