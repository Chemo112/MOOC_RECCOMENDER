from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
import os

db_host = os.environ.get('PGHOST')
db_port = os.environ.get('PGPORT')
db_name = os.environ.get('PGDATABASE')
db_user = os.environ.get('PGUSER')
db_password = os.environ.get('PGPASSWORD')

conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    dbname=db_name,
    user=db_user,
    password=db_password
)
'''
argomenti = ["Programming and software development", "Business and management",
             "Data science and artificial intelligence", "Engineering and technology", "Art and design",
             "Social sciences", "Languages and literature", "Mathematics and statistics", "Health sciences",
             "Physical and natural sciences"]
'''
import pandas as pd
DB = pd.read_csv("edx_courses.csv")
lista = [row for row in DB['subject']]
argomenti = sorted(list(set(lista)))


app = Flask(__name__)

app.secret_key = '000999'
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
    return User.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username

        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and password == user.password:
            login_user(user)
            return redirect(url_for('home'))
        else:
            return 'Invalid username or password'
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user:
            return 'Username already exists', render_template('login.html')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            session['username'] = username
            return redirect(url_for('home'))
    else:
        return render_template('register.html')


@app.route('/index', methods=['GET', 'POST'])
def home():
    selected_topics= []
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
        # return redirect(url_for('raccomandazioni2', argomenti=argomenti))
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
    data = request.args.to_dict()
    topics = [0 for _ in argomenti]
    user = User.query.filter_by(username=session['username']).first()
    session['id'] = user.id
   # user_exp = User_experience.query.filter_by(id=session['id']).all()

    user_exp = User_experience.query.filter_by(id=session['id']).first()
    tmpDict = dict()
    if user_exp:

        diz = vars(user_exp).copy()
        tmplist = diz.keys()
        for el in sorted(tmplist):
            print(el, "-----------------------------------------------------.............")
            i = int(el.strip("topic"))
            tmpDict[argomenti[i]] = diz[el]


        # prendiamo la prima configurazione di preferenze disponibile ma in futuro ne avremo più d'una per ogni utente
        # che col tempo incroceremo per creare in vero collaborative filtering
        session['experience'] = tmpDict
        return redirect(url_for('show_courses'))
    else:
        print("TODO")##da implementare il confronto tra le varie confiugurazioni configurazioni

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

    session['experience'] = topics
    return redirect(url_for('show_courses'))

#render_template('finale.html')



def reccomender(subjects_exp):
    dict_sbj = dict()
    res = dict()
    for sbj in subjects_exp:
        if subjects_exp[sbj] > 0:
            if subjects_exp[sbj] // 3 <=1:
                diff = "Introductory"
            else:
                if subjects_exp[sbj] // 3 <=2:
                    diff = "Intermediate"
                else:
                    diff = "Advanced"
            dict_sbj[sbj] = diff
    for sbj in dict_sbj:
        df = DB.loc[DB['subject'] == sbj]
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
        user_courses[subject] = selected_courses

    return render_template('show_courses.html', user_courses=user_courses)







if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=os.getenv("PORT", default=5000))
