import pandas as pd
import matplotlib.pyplot as plt
key = 'csvData'
df = pd.read_csv('static\cleantxt.txt', delimiter='\t\t', engine='python')
df.columns = ['name', 'year', 'room', 'mailroom', 'town', 'state', 'email']

table = pd.read_csv(f'{key}.csv')
states = table['Code'].values
dic = {}
sum = 0

for state in states:
    sum+=df.loc[df['state']==state].count()['name']
    dic[state] = df.loc[df['state']==state].count()['name']

for state in states:
    dic[state]/=sum
    dic[state]*=100
for state in states:
    if dic[state]<1:
        dic.pop(state)

fig1, ax1 = plt.subplots()
ax1.pie(list(dic.values()), labels=list(dic.keys()), autopct='%d%%', shadow=True, startangle=90)
ax1.axis('equal')
plt.title(f'Pie chart of the student\'s population\n\n')
plt.show()
