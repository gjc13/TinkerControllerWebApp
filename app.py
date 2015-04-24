from flask import Flask, render_template,url_for
from flask.ext.socketio import SocketIO, send, emit, join_room, leave_room,disconnect
import client
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
global currentuser 
currentuser = 01
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


@socketio.on('my event')
def handle_my_custom_event(json):
    global currentuser
    x = json[u'x']
    y = json[u'y']
    theta = json[u'theta']
    if (json[u'user'] == currentuser):
        print x,y,theta
        client.send("SetRobotSpeed Vx "+str(int(x)))
        client.send("SetRobotSpeed Vy "+str(int(y)))
        client.send("SetRobotSpeed Omega "+str(int(theta)))
    
@socketio.on('user')
def handle_user_event(json):
    print json[u'user'] , json[u'data']
    if json[u'data'] == "A user connected!":
        global currentuser
        currentuser = json[u'user']
        print 'current user is ', currentuser
    

if __name__ == '__main__':
    client.send("EnableSystem")
    socketio.run(app,host='0.0.0.0')