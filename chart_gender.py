import pandas as pd
import matplotlib.pyplot as plt

gender={'HO':'M', 'KE':'M', 'HI':'M', 'AL':'M', 'HA':'F', 'LI':'M', 'ME':'M', 'MP':'F', 'SO':'F', 'NO':'F', 'WE':'F', 'Co':'UN', 'CH':'UN'}

def get_states(key):
    table = pd.read_csv(f'{key}.csv')
    states = table['Code'].values
    return list(states)

key = 'csvData'
df = pd.read_csv('static\cleantxt.txt', delimiter='\t\t', engine='python')
df.columns = ['name', 'year', 'room', 'mailroom', 'town', 'state', 'email']

table = pd.read_csv(f'{key}.csv')
states = table['Code'].values
dic = {}
sum = 0
nmales = 0
nfemales = 0
regx_male = '((HO|KE|HI|AL|HA|LI|ME)[0-9][0-9][0-9](A|B))|(HO|KE|HI|AL|HA|LI|ME)[0-9][0-9][0-9]|((HO|KE|HI|AL|HA|LI|ME)[0-9][0-9](A|B))|(HO|KE|HI|AL|HA|LI|ME)[0-9][0-9]'
regx_female = '((MP|SO|NO|WE)[0-9][0-9][0-9](A|B))|((MP|SO|NO|WE)[0-9][0-9][0-9])|((MP|SO|NO|WE)[0-9][0-9](A|B))|((MP|SO|NO|WE)[0-9][0-9])'
for state in states:
    nmales+=df.loc[df['state']==state].loc[df['room'].str.match(regx_male)].count()['name']
    nfemales+= df.loc[df['state']==state].loc[df['room'].str.match(regx_female)].count()['name']


print(nmales+104)
print(nfemales+104)

val1 = nmales+104
val2 = nfemales+104

sum = val1 + val2
val1/=sum
val2/=sum
normal = [val1, val2]
genders = ['M', 'F']
print(normal)

fig1, ax1 = plt.subplots()
ax1.pie(normal, explode = (0.1,0), labels=genders, autopct='%d%%', shadow=True, startangle=90)
ax1.axis('equal')
plt.title(f'Pie chart of the student population distributed by gender \n\n')
plt.show()
