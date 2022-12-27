import pandas as pd
import matplotlib.pyplot as plt

key = 'west'
df = pd.read_csv('static\cleantxt.txt', delimiter='\t\t', engine='python')
df.columns = ['name', 'year', 'room', 'mailroom', 'town', 'state', 'email']

table = pd.read_csv(f'{key}.csv')
states = table['Code'].values


