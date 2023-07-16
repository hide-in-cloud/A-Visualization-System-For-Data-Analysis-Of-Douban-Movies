import re


data = ['1', '2']
languages = ''.split('/')
languages = ','.join([item.strip() for item in languages])
data.append(languages)
print(data)

comment_len = 'a'
comment_len = re.search('\d+', comment_len)
if comment_len:
    comment_len = comment_len.group()
else:
    comment_len = ''
data.append(comment_len)
print(data)

if comment_len != '' and int(comment_len) > 0:
    print(comment_len)


# print(data)
