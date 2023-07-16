import json
import pandas as pd
from sqlalchemy import create_engine

# mysql驱动引擎
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/douban_movie')
sql = 'select * from movie_detail;'
movie_detail = pd.read_sql(sql, engine)
movie_detail.set_index('id', inplace=True)
# print(movie_detail)

# 取出每部电影的短评
all_comments = movie_detail['comments'].apply(lambda x: json.loads(x))
# print(all_comments)
rows = []
for mid, movie_comments in all_comments.items():
    for user_comment in movie_comments:
        username = user_comment.get('user')
        comment_star = user_comment.get('comment_star')
        comment_content = user_comment.get('comment_content')
        comment_time = user_comment.get('comment_time')
        rows.append([username, mid, comment_star, comment_content, comment_time])
# 将数据写到新的DataFrame中
df_comments = pd.DataFrame(rows, columns=['username','movie_id','comment_star','comment_content','comment_time'])

# 按照username排序，然后对其编号，同一username为同一编号
df_comments.sort_values(by='username', inplace=True)
# print(df_comments)
Number = []
temp = df_comments['username'].tolist()
for i,v in enumerate(temp):
    if i == 0:
        Number.append(1)
    elif v == temp[i-1]:
        Number.append(Number[-1])
    else:
        Number.append(Number[-1]+1)
df_comments["username"] = Number

# 还原顺序
df_comments.sort_index(inplace=True)
df_comments['comment_content'] = df_comments['comment_content'].apply(lambda x: json.dumps(x))
print(df_comments)

# 存入数据库
# df_comments.to_sql('movie_comment', con=engine, index=False, if_exists='append')
