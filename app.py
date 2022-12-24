from flask import Flask, request, render_template, redirect, url_for, abort
from forms import question
import pandas as pd
from student import student

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'aquickbrownfoxjumpedoverthelazydog'


df = pd.read_csv('static/cleantxt.txt', delimiter='\t\t', engine='python')
df.columns = ['name', 'year', 'room', 'mailroom', 'town', 'state', 'email']

@app.route('/', methods=["GET"])
def get_home():
    form = question()
    return render_template('home.html', form=form)

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
    dic={'GR':'Graduate', 'FF': 'Freshman', 'FR': 'Freshman', 'SO': 'Sophomore', 'JR':'Junior', 'SR':'Senior'}
    dorms = {'HO':'Hopeman', 'KE':'Ketler', 'HI':'Hicks','AL':'Alumni', 'HA':'Harker', 'LI':'Lincoln',
         'ME':'Memorial', 'MP':'MAP', 'SO':'South MEP', 'NO':'North MEP', 'WE':'West MEP',
         'Co': 'Not living on campus', 'CH':'Colonial Hall' }
    for index, row in frame.iterrows():
        state = ''
        if str(row['state']).strip()=='nan':
            state ='nan'
        else:
            state = row['state']
        temp = student(row['name'], row['year'], row['town'], state, row['email'], row['mailroom'], row['room'])
        roomates = get_roomates(row['room'])
    return render_template('profile.html', student=temp, dic=dic, dorms=dorms, roomates=roomates)

def get_roomates(room):
    students = []
    print(room)
    if(room[len(room)-1] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        room = room[:-1]
    frame = df.loc[df['room'].str.contains(room)]
    for index, row in frame.iterrows():
        students.append(student(row['name'], row['year'], row['town'], row['state'], row['email'], row['mailroom'], row['room']))
    return students
