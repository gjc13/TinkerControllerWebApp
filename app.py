from flask import Flask, render_template,url_for,request
#from flask.ext.socketio import SocketIO, send, emit, join_room, leave_room,disconnect
import client
from threading import Timer
from collections import deque

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
global maxuserid 
maxuserid = 1
global currentuser
currentuser = 0
global waiting_users
waiting_users = deque()
global is_using
is_using = False
global expire_timer
expire_timer = None


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/touchtest')
def touchtest():
    return render_template("Touches.html")
    
@app.route('/touch')
def touch():
    return render_template("TouchControl.html")

@app.route('/controller')
def control():
    return render_template("Controller.html")


@app.route('/command/<cmd_data>')
def command(cmd_data):
    data_list = cmd_data.split(',')
    uid = int(data_list[0])
    if (uid == currentuser and is_using):
        x = float(data_list[1])
        y = float(data_list[2])
        theta = float(data_list[3])
        client.send("SetRobotSpeed Vx "+str(int(y)))
        client.send("SetRobotSpeed Vy "+str(int(x)))
        client.send("SetRobotSpeed Omega "+str(int(-theta)))
    return ""


@app.route('/login')
def login():
    global is_using, currentuser, maxuserid, waiting_users
    maxuserid += 1
    if is_using:
        waiting_users.put(maxuserid)
    else:
        set_user(maxuserid)
    return str(maxuserid)


@app.route('/logout/<int:userid>')
def logout(userid):
    global is_using, expire_timer, currentuser, waiting_users
    if userid is currentuser:
        clear_user()
        expire_timer.cancel()
    else:
        waiting_users.remove(userid)
    return ""


def set_user(uid):
    global is_using, expire_timer, currentuser
    if is_using:
        return
    currentuser = uid
    print '{0} connected'.format(currentuser)
    is_using = True
    if expire_timer is not None:
        expire_timer.cancel()
    expire_timer = Timer(60, clear_user)
    expire_timer.start()


def clear_user():
    global is_using
    if is_using:
        print '{0} cleared'.format(currentuser)
        is_using = False
        if len(waiting_users) > 0:
            new_user = waiting_users[0]
            waiting_users.popleft()
            set_user(new_user)



#@socketio.on('join')
#def on_join(data):
#    username = data['username']
#    #room = data['room']
#    room = '407'
#    join_room(room)
#    send(username + ' has entered the room.', room=room)
#
#@socketio.on('leave')
#def on_leave(data):
#    username = data['username']
#    #room = data['room']
#    room = '407'
#    leave_room(room)
#    send(username + ' has left the room.', room=room)


# @socketio.on('my event')
# def handle_my_custom_event(json):
#     global currentuser
#     x = json[u'x']
#     y = json[u'y']
#     theta = json[u'theta']
#     if (json[u'user'] == currentuser):
#         print x,y,theta
#         client.send("SetRobotSpeed Vx "+str(int(y)))
#         client.send("SetRobotSpeed Vy "+str(int(x)))
#         client.send("SetRobotSpeed Omega "+str(int(-theta)))
#     
# @socketio.on('user')
# def handle_user_event(json):
#     print json[u'user'] , json[u'data']
#     if json[u'data'] == "A user connected!":
#         global currentuser
#         currentuser = json[u'user']
#         client.send("EnableSystem")
#         print 'current user is ', currentuser
    

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = False)
#    socketio.run(app,host='0.0.0.0')
