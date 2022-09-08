from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/bnchmrk'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

def formatArray(array):
    array = str(array)
    array = array.replace('[','{')
    array = array.replace(']','}')
    return array


@app.route('/')
def index():
    return '<h1>Hello World</h1>'

#get user's username given email
@app.route('/getusername', methods = ['GET'])
def getusername():
    id = request.args.get('id')
    connection = db.session.connection()
    query = text(f"SELECT username FROM users WHERE id='{id}';")
    execute = connection.execute(query)
    result = execute.fetchone()
    resultstring = str(result)
    return resultstring[2:-3]

#get user's email given user id
@app.route('/getemail', methods = ['GET'])
def getemail():
    id = request.args.get('id')
    connection = db.session.connection()
    query = text(f"SELECT email FROM users WHERE id='{id}';")
    execute = connection.execute(query)
    result = execute.fetchone()
    resultstring = str(result)
    return resultstring[2:-3]

#get user's weight given user id
@app.route('/getweight', methods = ['GET'])
def getweight():
    id = request.args.get('id')
    connection = db.session.connection()
    query = text(f"SELECT weight FROM users WHERE id='{id}';")
    execute = connection.execute(query)
    result = execute.fetchone()
    resultstring = str(result)
    return resultstring[1:-2]

#get user's squat pr given user id
@app.route('/getsquatpr', methods = ['GET'])
def getsquatpr():
    id = request.args.get('id')
    connection = db.session.connection()
    query = text(f"SELECT squatpr FROM users WHERE id='{id}';")
    execute = connection.execute(query)
    result = execute.fetchone()
    resultstring = str(result)
    return resultstring[1:-2]

#get user's bench pr given user id
@app.route('/getbenchpr', methods = ['GET'])
def getbenchpr():
    id = request.args.get('id')
    connection = db.session.connection()
    query = text(f"SELECT benchpr FROM users WHERE id='{id}';")
    execute = connection.execute(query)
    result = execute.fetchone()
    resultstring = str(result)
    return resultstring[1:-2]

#get user's deadlift pr given user id
@app.route('/getdeadliftpr', methods = ['GET'])
def getdeadliftpr():
    id = request.args.get('id')
    connection = db.session.connection()
    query = text(f"SELECT deadliftpr FROM users WHERE id='{id}';")
    execute = connection.execute(query)
    result = execute.fetchone()
    resultstring = str(result)
    return resultstring[1:-2]

#get all user's lifts given user id
@app.route('/getuserlifts', methods = ['GET'])
def getuserlifts():
    id = request.args.get('id')
    connection = db.session.connection()
    query = text(f"SELECT * FROM lifts WHERE user_id='{id}';")
    execute = connection.execute(query)
    result = execute.fetchall()
    resultstring = str(result)
    return resultstring

#get all user's squats given user id
@app.route('/getusersquats', methods = ['GET'])
def getusersquats():
    id = request.args.get('id')
    connection = db.session.connection()
    query = text(f"SELECT * FROM lifts WHERE user_id='{id}' AND lift_type='squat';")
    execute = connection.execute(query)
    result = execute.fetchall()
    resultstring = str(result)
    return resultstring

#get all user's bench's given user id
@app.route('/getuserbenchs', methods = ['GET'])
def getusersbenchs():
    id = request.args.get('id')
    connection = db.session.connection()
    query = text(f"SELECT * FROM lifts WHERE user_id='{id}' AND lift_type='benchpress';")
    execute = connection.execute(query)
    result = execute.fetchall()
    resultstring = str(result)
    return resultstring

#get all user's deadlifts given user id
@app.route('/getuserdeadlifts', methods = ['GET'])
def getuserdeadlifts():
    id = request.args.get('id')
    connection = db.session.connection()
    query = text(f"SELECT * FROM lifts WHERE user_id='{id}' AND lift_type='deadlift';")
    execute = connection.execute(query)
    result = execute.fetchall()
    resultstring = str(result)
    return resultstring

#get all user's PR's given user id


#add new user
@app.route('/adduser', methods = ['POST'])
def adduser():
    id = request.args.get('id')
    username = request.args.get('username')
    email = request.args.get('email')
    firstname = request.args.get('firstname')
    lastname = request.args.get('lastname')
    weight = request.args.get('weight')
    height = request.args.get('height')
    age = request.args.get('age')
    squatpr = request.args.get('squatpr')
    benchpr = request.args.get('benchpr')
    deadliftpr = request.args.get('deadliftpr')
    gender = request.args.get('gender')

    query = text(f"INSERT INTO users VALUES ('{id}', '{username}', '{email}', '{firstname}', '{lastname}', {weight}, {height}, {age}, {squatpr}, {benchpr}, {deadliftpr}, {gender});")
    db.engine.execute(query)
    
    return "added user"

#add new lift
@app.route('/addlift', methods = ['POST'])
def addlift():
    id = request.args.get('id')
    user_id = request.args.get('user_id')
    lift_type = request.args.get('lift_type')
    lift_name = request.args.get('lift_name')
    weight = request.args.get('weight')

    query = text(f"INSERT INTO lifts VALUES ('{id}', '{user_id}', '{lift_type}', '{lift_name}', {weight});")
    db.engine.execute(query)
    
    return "added lift"

#get array of points for a squat with lift id
@app.route('/getsquatdata', methods = ['GET'])
def getsquatdata():
    id = request.args.get('id')
    connection = db.session.connection()
    query = text(f"SELECT * FROM squat_data WHERE lift_id = '{id}';")
    execute = connection.execute(query)
    result = execute.fetchone()
    resultstring = str(result)
    return resultstring

#post array of points for a squat with lift id
@app.route('/addsquatdata', methods = ['POST'])
def addsquatdata():
    content = request.json

    print(content)

    squat_id = content['squat_id']
    id = content['id']
    is_good_lift = content['is_good_lift']
    time = formatArray(content['time'])
    hip_locations = formatArray(content['hip_locations'])
    knee_locations = formatArray(content['knee_locations'])
    knee_angles = formatArray(content['knee_angles'])
    time_under_parallel = content['time_under_parallel']
    justification = formatArray(content['justification'])
    reps = content['reps']
    
    print(f"{squat_id}\n")
    print(f"{id}\n")
    print(f"{is_good_lift}\n")
    print(f"{time}\n")
    print(f"{hip_locations}\n")
    print(f"{knee_locations}\n")
    print(f"{knee_angles}\n")
    print(f"{time_under_parallel}\n")
    print(f"{justification}\n")
    print(f"{reps}\n")

    #logging.info(squat_id,id,is_good_lift,time,hip_locations,knee_locations,knee_angles,time_under_parallel,justification,reps)

    query = text(f"INSERT INTO squat_data VALUES ('{squat_id}',{id},{is_good_lift},'{time}','{hip_locations}','{knee_locations}','{knee_angles}',{time_under_parallel},{reps},'{justification}');")
    db.engine.execute(query)
    return "added squat data"

#get array of points for a bench with lift id
@app.route('/getbenchdata', methods = ['GET'])
def getbenchdata():
    id = request.args.get('id')
    connection = db.session.connection()
    query = text(f"SELECT * FROM bench_data WHERE lift_id = '{id}';")
    execute = connection.execute(query)
    result = execute.fetchone()
    resultstring = str(result)
    return resultstring

#post array of points for a bench with lift id
@app.route('/addbenchdata', methods = ['POST'])
def addbenchdata():
    bench_id = request.args.get('bench_id')
    id = request.args.get('id')
    is_good_lift = request.args.get('is_good_lift')
    time = request.args.get('time')
    bar_locations = request.args.get('bar_locations')
    chest_locations = request.args.get('chest_locations')
    arm_angles = request.args.get('arm_angles')
    time_on_chest = request.args.get('time_on_chest')
    justification = request.args.get('justification')
    reps = request.args.get('reps')

    query = text(f"INSERT INTO bench_data VALUES ('{bench_id}','{id}',{is_good_lift},'{time}','{bar_locations}','{chest_locations}','{arm_angles}',{time_on_chest},'{justification}',{reps});")
    db.engine.execute(query)
    return "added bench data"

if __name__ == '__main__':
    app.run(debug=True)