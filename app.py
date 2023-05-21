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
argomenti = ["Programming and software development", "Business and management", "Data science and artificial intelligence", "Engineering and technology", "Art and design", "Social sciences", "Languages and literature", "Mathematics and statistics", "Health sciences", "Physical and natural sciences"]

app = Flask(__name__)

app.secret_key = '000999'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://'+db_user+':'+db_password+'@'+db_host+':'+db_port+'/'+db_name
db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    @property
    def is_active(self):
        return True
class User_preferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic1 = db.Column(db.Integer, nullable=True)
    topic2 = db.Column(db.Integer, nullable=True)
    topic3 = db.Column(db.Integer, nullable=True)
    topic4 = db.Column(db.Integer, nullable=True)
    topic5 = db.Column(db.Integer, nullable=True)
    topic6 = db.Column(db.Integer, nullable=True)
    topic7 = db.Column(db.Integer, nullable=True)
    topic8 = db.Column(db.Integer, nullable=True)
    topic9 = db.Column(db.Integer, nullable=True)
    topic10 = db.Column(db.Integer, nullable=True)
    username = db.Column(db.String(50), unique=True)


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
    selezionati = []
    if request.method == 'POST':
        # se l'utente ha selezionato degli argomenti, crea una lista di argomenti selezionati
        selezionati = request.form.getlist('argomenti')
        return render_template('raccomandazioni2.html', argomenti=selezionati)
    else:
        return render_template('selezione2.html', argomenti=argomenti)

@login_required
@app.route('/esperienza', methods=['GET', 'POST'])
def esperienza():
    argomenti = request.args.getlist('argomenti')
    if request.method == 'POST':
        # Gestisci i dati del form in modo appropriato
        #return redirect(url_for('raccomandazioni2', argomenti=argomenti))
        return render_template('esperienza.html', argomenti=argomenti)

    elif request.method == 'GET':
        if request.args.get('esp'):
            # Se esp è True, indirizza l'utente alla pagina esperienza.html
            return render_template('esperienza.html', argomenti=argomenti)
        else:
            # Altrimenti, indirizza l'utente alla pagina raccomandazioni.html
            return render_template('raccomandazioni2.html', argomenti=argomenti)

@login_required
@app.route('/salva-esperienza', methods=['GET'])

def salva_esperienza():
    data = request.args.to_dict()
    topics = [0 for _ in argomenti]

    max_id = db.session.query(db.func.max(User_preferences.id)).scalar()

    user_exists = User_preferences.query.filter_by(username=session['username']).first()

    if user_exists:
        return render_template('finale.html')

    for key in data.keys():
        topics[argomenti.index(key)] = int(data[key])
        new_pref = User_preferences(id=max_id+1,topic1=topics[0],
                                         topic2=topics[1],
                                         topic3=topics[2],
                                         topic4=topics[3],
                                         topic5=topics[4],
                                         topic6=topics[5],
                                         topic7=topics[6],
                                         topic8=topics[7],
                                         topic9=topics[8],
                                         topic10=topics[9],
                                         username=session['username'])
    db.add(new_pref)
    db.session.commit()

    return render_template('finale.html')



import os
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=os.getenv("PORT", default=5000))
