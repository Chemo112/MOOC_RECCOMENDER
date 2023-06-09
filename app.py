from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, UserMixin
import os
from flask_bcrypt import Bcrypt

db_host = os.environ.get('PGHOST')
db_port = os.environ.get('PGPORT')
db_name = os.environ.get('PGDATABASE')
db_user = os.environ.get('PGUSER')
db_password = os.environ.get('PGPASSWORD')
key = os.environ.get("FLASKKEY")
conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    dbname=db_name,
    user=db_user,
    password=db_password
)

app = Flask(__name__)
bcrypt = Bcrypt(app)

import pandas as pd

DB = pd.read_csv("courses.csv")
lista = [row for row in DB['subject']]
argomenti = sorted(list(set(lista)))

app.secret_key = str(key)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + db_user + ':' + db_password + '@' + db_host + ':' + db_port + '/' + db_name

db = SQLAlchemy(app)
login_manager = LoginManager(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    @property
    def is_active(self):
        return True


class User_experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic1 = db.Column(db.Integer, nullable=False)
    topic2 = db.Column(db.Integer, nullable=False)
    topic3 = db.Column(db.Integer, nullable=False)
    topic4 = db.Column(db.Integer, nullable=False)
    topic5 = db.Column(db.Integer, nullable=False)
    topic6 = db.Column(db.Integer, nullable=False)
    topic7 = db.Column(db.Integer, nullable=False)
    topic8 = db.Column(db.Integer, nullable=False)
    topic9 = db.Column(db.Integer, nullable=False)
    topic10 = db.Column(db.Integer, nullable=False)
    topic11 = db.Column(db.Integer, nullable=False)
    topic12 = db.Column(db.Integer, nullable=False)
    topic13 = db.Column(db.Integer, nullable=False)
    topic14 = db.Column(db.Integer, nullable=False)
    topic15 = db.Column(db.Integer, nullable=False)
    topic16 = db.Column(db.Integer, nullable=False)
    topic17 = db.Column(db.Integer, nullable=False)
    topic18 = db.Column(db.Integer, nullable=False)
    topic19 = db.Column(db.Integer, nullable=False)
    topic20 = db.Column(db.Integer, nullable=False)
    topic21 = db.Column(db.Integer, nullable=False)
    topic22 = db.Column(db.Integer, nullable=False)
    topic23 = db.Column(db.Integer, nullable=False)
    topic24 = db.Column(db.Integer, nullable=False)
    topic25 = db.Column(db.Integer, nullable=False)
    topic26 = db.Column(db.Integer, nullable=False)
    topic27 = db.Column(db.Integer, nullable=False)
    topic28 = db.Column(db.Integer, nullable=False)
    topic29 = db.Column(db.Integer, nullable=False)
    topic30 = db.Column(db.Integer, nullable=False)
    topic31 = db.Column(db.Integer, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        password = request.form['password']
        user = db.session.query(User).filter(User.username == session['username']).first()
        try:
            check = bcrypt.check_password_hash(user.password, password)
        except Exception as e:
            return render_template('login_fail.html')
            print(e)

        if user and check:
            print("sono entrato")
            login_user(user)
            return redirect(url_for('home'))
        else:
            return render_template('login_fail.html')
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        session['username'] = username
        user = db.session.query(User).filter(User.username == username).first()

        if user:
            return render_template('register_fail.html')
        else:
            pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, password=pw_hash)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            session['username'] = username
            return redirect(url_for('home'))
    else:
        return render_template('register.html')


@app.route('/index', methods=['GET', 'POST'])
def home():
    selected_topics = []
    if request.method == 'POST':
        # se l'utente ha selezionato degli argomenti, crea una lista di argomenti selezionati
        selected_topics = request.form.getlist('argomenti')
        return render_template('summary.html', argomenti=selected_topics)
    else:
        return render_template('selection.html', argomenti=argomenti)


@login_required
@app.route('/experience', methods=['GET', 'POST'])
def esperienza():
    argomenti = request.args.getlist('argomenti')
    if request.method == 'POST':
        # Gestisci i dati del form in modo appropriato
        return render_template('experience.html', argomenti=argomenti)

    elif request.method == 'GET':
        if request.args.get('esp'):
            # Se esp è True, indirizza l'utente alla pagina experience.html
            return render_template('experience.html', argomenti=argomenti)
        else:
            # Altrimenti, indirizza l'utente alla pagina summary.html
            return render_template('summary.html', argomenti=argomenti)


@login_required
@app.route('/save_experience', methods=['GET'])
def save_experience():
    Session = db.session()
    data = request.args.to_dict()
    topics = [0 for _ in argomenti]
    user = Session.query(User).filter(User.username == session['username']).first()
    session['id'] = user.id
    user_exp = Session.query(User_experience).filter(User_experience.id == session['id']).first()

    if user_exp:
        tmpDict = dict()
        tmpDict[argomenti[0]] = user_exp.topic1
        tmpDict[argomenti[1]] = user_exp.topic2
        tmpDict[argomenti[2]] = user_exp.topic3
        tmpDict[argomenti[3]] = user_exp.topic4
        tmpDict[argomenti[4]] = user_exp.topic5
        tmpDict[argomenti[5]] = user_exp.topic6
        tmpDict[argomenti[6]] = user_exp.topic7
        tmpDict[argomenti[7]] = user_exp.topic8
        tmpDict[argomenti[8]] = user_exp.topic9
        tmpDict[argomenti[9]] = user_exp.topic10
        tmpDict[argomenti[10]] = user_exp.topic11
        tmpDict[argomenti[11]] = user_exp.topic12
        tmpDict[argomenti[12]] = user_exp.topic13
        tmpDict[argomenti[13]] = user_exp.topic14
        tmpDict[argomenti[14]] = user_exp.topic15
        tmpDict[argomenti[15]] = user_exp.topic16
        tmpDict[argomenti[16]] = user_exp.topic17
        tmpDict[argomenti[17]] = user_exp.topic18
        tmpDict[argomenti[18]] = user_exp.topic19
        tmpDict[argomenti[19]] = user_exp.topic20
        tmpDict[argomenti[20]] = user_exp.topic21
        tmpDict[argomenti[21]] = user_exp.topic22
        tmpDict[argomenti[22]] = user_exp.topic23
        tmpDict[argomenti[23]] = user_exp.topic24
        tmpDict[argomenti[24]] = user_exp.topic25
        tmpDict[argomenti[25]] = user_exp.topic26
        tmpDict[argomenti[26]] = user_exp.topic27
        tmpDict[argomenti[27]] = user_exp.topic28
        tmpDict[argomenti[28]] = user_exp.topic29
        tmpDict[argomenti[29]] = user_exp.topic30
        tmpDict[argomenti[30]] = user_exp.topic31
        # prendiamo la prima configurazione di preferenze disponibile ma in futuro ne avremo più d'una per ogni utente
        # che col tempo incroceremo per creare in vero collaborative filtering
        session['experience'] = tmpDict
        return redirect(url_for('show_courses'))
    else:
        print("TODO")  ##da implementare il confronto tra le varie confiugurazioni configurazioni

    for sbj in data.keys():
        topics[argomenti.index(sbj)] = int(data[sbj])
        new_pref = User_experience(id=user.id,
                                   topic1=topics[0],
                                   topic2=topics[1],
                                   topic3=topics[2],
                                   topic4=topics[3],
                                   topic5=topics[4],
                                   topic6=topics[5],
                                   topic7=topics[6],
                                   topic8=topics[7],
                                   topic9=topics[8],
                                   topic10=topics[9],
                                   topic11=topics[10],
                                   topic12=topics[11],
                                   topic13=topics[12],
                                   topic14=topics[13],
                                   topic15=topics[14],
                                   topic16=topics[15],
                                   topic17=topics[16],
                                   topic18=topics[17],
                                   topic19=topics[18],
                                   topic20=topics[19],
                                   topic21=topics[20],
                                   topic22=topics[21],
                                   topic23=topics[22],
                                   topic24=topics[23],
                                   topic25=topics[24],
                                   topic26=topics[25],
                                   topic27=topics[26],
                                   topic28=topics[27],
                                   topic29=topics[28],
                                   topic30=topics[29],
                                   topic31=topics[30])

    db.session.add(new_pref)
    db.session.commit()
    subject_exp = dict()

    for i in range(len(topics)):
        subject_exp[argomenti[i]] = topics[i]

    session['experience'] = subject_exp
    return redirect(url_for('show_courses'))


def reccomender(subjects_exp):
    dict_sbj = dict()
    res = dict()
    for sbj in subjects_exp:
        if subjects_exp[sbj] > 0:
            if subjects_exp[sbj] // 3 <= 1:
                diff = "Introductory"
            else:
                if subjects_exp[sbj] // 3 <= 2:
                    diff = "Intermediate"
                else:
                    diff = "Advanced"
            dict_sbj[sbj] = diff
    for sbj in dict_sbj:
        df = DB.loc[DB['subject'] == sbj]
        df.fillna('Description is Missing', inplace=True)

        df1 = df.loc[df['Level'] == dict_sbj[sbj]]
        res[sbj] = df1
    return res


@login_required
@app.route('/show_courses', methods=['GET'])
def show_courses():
    courses = reccomender(session['experience'])
    user_courses = {}
    for subject, courses_df in courses.items():
        selected_courses = courses_df
        if len(selected_courses) > 0:
            user_courses[subject] = selected_courses

    return render_template('show_courses.html', user_courses=user_courses)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=os.getenv("PORT", default=5000))
