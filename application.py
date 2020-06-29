import os

from flask import Flask, request, render_template, redirect, session, jsonify
from flask_session import Session
from flask_socketio import SocketIO, emit
from collections import deque
from functions import * 

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

#configure session to use file system.
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

#our storage data structures
messages = {'cs50': deque([], maxlen=100)}
channels = {'cs50': ['Brian', 'Eric', 'Jose', 'Cynthia']}
users = {1: 'Brian', 2: 'Eric', 3: 'Jose', 4: 'Cynthia'}
direct = {'Brian': {'Eric': []}}

@app.route('/')
@login_required
def index():
    current_user = users[session['user_id']]
    return render_template('layout.html', user = current_user)


@app.route("/channels")
@login_required
def channel():
    if request.method == 'GET':
        #knowing channels and number of users
        included = []
        non = []
        for (key, value) in channels.items():
            if users[session['user_id']] in value:
                included.append([key, len(value)])
            else:
                non.append([key, len(value)])
        #knowing the users that share the same channel with the current user.
        direct = []
        for values in channels.values():
            if users[session['user_id']] in values:
                for user in values:
                    if user != users[session['user_id']]:
                        direct.append(user)
        #return a list of the channels
        return jsonify([included, non, direct])
    

@app.route('/channel', methods = ['POST'])
@login_required
def newChannel():
    channel = request.form.get('channel')
    user_id = session['user_id']

    user_name = users[user_id]
    #check if channel doesn't exist already
    if channel in channels:
        return jsonify({'success': 'no'})
    else:
        #now insert the channel into the channels & messages dictionary
        channels[channel] = [user_name]
        messages[channel] = deque(maxlen=100)

        #data to broadcast.
        data = {'success': 'yes', 'messages': False, 'admin': user_name, 'channel': channel}

        return jsonify(data)

@app.route('/direct', methods = ['POST'])
@login_required
def direct_user():
    name = request.form.get('name')
    current_user = users[session['user_id']]

    #insert the new direct user if not already and get their messages
    if name not in direct.keys() and current_user not in direct.keys():
        direct[current_user] = {name: []}
        messages = []
    else:
        try:
            if current_user not in list(direct[name].keys()):
                #insert the user in
                direct[name][current_user] = []
                messages = []
            else:
                #get messages
                messages = direct[name][current_user]
        except KeyError:
            if name not in list(direct[current_user].keys()):
                #insert the other user in
                direct[current_user][name] = []
                messages = []
            else:
                #get messages
                messages = direct[current_user][name]
    #data about private chat messaging to send back
    data = {'current': current_user, 'other': name, 'messages': messages}
    return jsonify(data)


@app.route('/login', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('hello.html')
    else:
        name = request.form.get('name')
        if name in users.values():
            for (key, value) in users.items():
                if value == name:
                    user_id = key
            session['user_id'] = user_id
            return redirect("/")
        else:
            return render_template('hello.html', message = "Name not recognized!")

@app.route('/register', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('hello.html')
    else:
        name = request.form.get('newName')
        if name not in users.values():
            i = int(len(users) + 1)
            users[i] = name
            session['user_id'] = i
            return redirect('/')
        else:
            return render_template('hello.html', message1 = 'User already exists!')


@app.route('/logout')
@login_required
def logout():
    #Clear sessions
    session.clear()
    #redirect to login
    return redirect('/')

@app.route('/charts', methods = ['POST'])
@login_required
def get_messages():
    channel = request.form.get('channel')
    #register the user if new to channel
    user_name = users[session['user_id']]
    if user_name not in channels[channel]:
        channels[channel].append(user_name)

    #private message users
    direct = []
    for values in channels.values():
        if users[session['user_id']] in values:
            for user in values:
                if user != users[session['user_id']]:
                    direct.append(user)

    admin = channels[channel][0]
    data = {'channel': channel, 'charts': list(messages[channel]),
            'users': list(channels[channel]), 'admin': admin, 'direct': direct}

    return jsonify(data)


@socketio.on('private message')
@login_required
def private_message(data):
    #insert the message into the direct dictionary for private messages
    other_user = data['user'] 
    current_user = users[session['user_id']]
    try:
        direct[current_user][other_user].append([current_user, data['message'], data['time']])
    except KeyError:
        direct[other_user][current_user].append([current_user, data['message'], data['time']])

    #message details to send back
    message = [other_user, current_user, data['message'], data['time']]   
    return emit('new private_message', message, broadcast = True)

@socketio.on('send message')
@login_required
def message(data):
    channel = data['channel']
    #get user credentials
    user_id = session['user_id']
    user = users[user_id]

    message = data['message']
    time = data['time']
    
    #we should first check if the channel exists. If not it should return an error
    if channel in channels:
        messages[channel].append([user, message, time]) 

        #create the data to send back
        data = [channel, user, message, time]
        return emit('receive message', data, broadcast=True)


