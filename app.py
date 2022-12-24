from flask import Flask, request, render_template, redirect, url_for, abort
from forms import question
import pandas as pd
from student import student

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'aquickbrownfoxjumpedoverthelazydog'

def split(word):
    return word.split()
def replace(word):
    word.replace(",", '')
    word.replace("\"", '')
    return word

app.jinja_env.globals.update(split=split, replace=replace)

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
        return render_template('results.html', students = students)
    else:
        return "error"

def get_student(name):
    students = []
    name = name.split()
    frames = df
    for el in name:
        frames = frames.loc[frames['name'].str.contains(el.capitalize())]
    for index, row in frames.iterrows():
        temp = student(row['name'], row['year'], row['town'], row['state'], row['email'])
        students.append(temp)
    return students

@app.route('/profile/<string:name>')
def get_profile(name):
    print(name)
    frame = df.loc[df['name'].str.contains(name)]
    print(frame)
    temp = None
    for index, row in frame.iterrows():
        print(row['name'], row['year'], row['town'], row['state'], row['email'])
        temp = student(row['name'], row['year'], row['town'], row['state'], row['email'])
    return render_template('profile.html', student=temp)
