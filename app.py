from flask import Flask, request, render_template, redirect, url_for, abort
from forms import question
import pandas as pd
from student import student
import os 
import re

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'aquickbrownfoxjumpedoverthelazydog'

dorms = {'HO':'Hopeman', 'KE':'Ketler', 'HI':'Hicks','AL':'Alumni', 'HA':'Harker', 'LI':'Lincoln',
         'ME':'Memorial', 'MP':'MAP', 'SO':'South MEP', 'NO':'North MEP', 'WE':'West MEP',
         'Co': 'Not living on campus', 'CH':'Colonial Hall' }

df = pd.read_csv('static/cleantxt.txt', delimiter='\t\t', engine='python')
df.columns = ['name', 'year', 'room', 'mailroom', 'town', 'state', 'email']
list_dorm = {}

@app.route('/', methods=["GET"])
def get_home():
    form = question()
    charts = []
    for file in os.listdir('./static/'):
        print(file)
        if re.search('_chart', file):
            charts.append(file)
    print(charts)
    return render_template('home.html', form=form, charts=charts)

@app.route('/', methods=["POST"])
def post_home():
    form=question()
    if form.validate():
        name = str(form.field.data)
        students = get_student(name)
        return render_template('results.html', students = students, length=len(students))
    else:
        return "error"

def get_student(name):
    students = []
    name = name.split()
    frames = df
    for el in name:
        frames = frames.loc[frames['name'].str.contains(el.capitalize())]
    for index, row in frames.iterrows():
        temp = student(row['name'], row['year'], row['town'], row['state'], row['email'], row['mailroom'], row['room'])
        students.append(temp)
    return students

@app.route('/profile/<string:name>')
def get_profile(name):
    frame = df.loc[df['name'].str.contains(name)]
    temp = None
    dic={'GR':'Graduate', 'FF': 'Freshman', 'FR': 'Freshman', 'SO': 'Sophomore', 'JR':'Junior', 'SR':'Senior', 'SS': 'Senior'}
    gender={'HO':'M', 'KE':'M', 'HI':'M', 'AL':'M', 'HA':'F', 'LI':'M', 'ME':'M', 'MP':'F', 'SO':'F', 'NO':'F', 'WE':'F', 'Co':'UN', 'CH':'UN'}
    for index, row in frame.iterrows():
        state = ''
        if str(row['state']).strip()=='nan':
            state ='nan'
        else:
            state = row['state']
        temp = student(row['name'], row['year'], row['town'], state, row['email'], row['mailroom'], row['room'])
        roomates = get_roomates(row['room'])
        if len(roomates)==1:
            roomates = None
    return render_template('profile.html', student=temp, dic=dic, dorms=dorms, roomates=roomates)

def get_roomates(room):
    students = []
    print(room)
    has_letters = False
    new_room=room
    if(room[len(room)-1] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        new_room = room[:-1]
        has_letters = True
    if len(new_room[2:])!=2:
        frame = df.loc[df['room'].str.contains(new_room)]
        print(frame)
    elif len(new_room[2:])==2 and has_letters:
        frame = df.loc[df['room'].str.contains(new_room)].loc[df['room'].str.match('[A-Z][A-Z][1-9][1-9](A|B)')]
    elif len(new_room[2:])==2 and not has_letters:
        frame = df.loc[df['room'].str.contains(new_room)].loc[df['room'].str.endswith(room)]
    for index, row in frame.iterrows():
        students.append(student(row['name'], row['year'], row['town'], row['state'], row['email'], row['mailroom'], row['room']))
    return students

def get_states(key):
    table = pd.read_csv(f'{key}.csv')
    states = table['Code'].values
    return list(states)

@app.route('/dorm/<string:population>/<string:dorm>')
def get_dorm(population, dorm):
    return render_template('dorm_list.html', population=population,dorm=dorm, list_student=list_dorm[dorm])
    return list_dorm[population]


@app.route('/population/<string:population>')
def get_population(population):
    table = pd.read_csv(f'{population}.csv')
    states = table['Code'].values
    students = []
    for index, row in df.iterrows():
        if row['state'] in states:
            students.append(student(row['name'], row['year'], row['town'], row['state'], row['email'], row['mailroom'], row['room']))
    distribution_dorm = {}
    for state in states:
        frame = df.loc[df['state']==state]
        for dorm in dorms.keys():
            if dorms[dorm] in distribution_dorm.keys():
                temp = frame.loc[frame['room'].str.contains(dorm)]
                print(temp)
                distribution_dorm[dorms[dorm]]+= temp.count()['name']
                list_dorm[dorms[dorm]].extend(temp.values.tolist())
            else:
                temp = frame.loc[frame['room'].str.contains(dorm)]
                print(temp)                
                distribution_dorm[dorms[dorm]]= temp.count()['name']
                list_dorm[dorms[dorm]] = temp.values.tolist()
    return render_template('populations.html', list_dorm=list_dorm, population=population, students=students, length=len(students), dic=distribution_dorm)
