import asyncio
import websockets
import json
import time
from geometry_msgs.msg import Twist
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse


def convertVelToCmd_vel(x=0,y=0,w=0):
  twist_msg = Twist()
  twist_msg.linear.x = x
  twist_msg.linear.y = y
  twist_msg.angular.z = w
  return {'linear': {'x': twist_msg.linear.x, 'y': twist_msg.linear.y, 'z': twist_msg.linear.z},'angular': {'x': twist_msg.angular.x, 'y': twist_msg.angular.y, 'z': twist_msg.angular.z}}

app = FastAPI()

html1 = """
<!DOCTYPE html>
<html>
    <head>
        <title>ROS WEB</title>
         <script type="text/javascript" src="http://static.robotwebtools.org/roslibjs/current/roslib.js"></script>
        <script src="http://static.robotwebtools.org/EventEmitter2/current/eventemitter2.js"></script>
    </head>
    <body>
        <h1>WebSocket Velocity</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="number" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""
html = """
<html>
    <head>
        <script type="text/javascript" src="http://static.robotwebtools.org/roslibjs/current/roslib.js"></script>
        <script src="http://static.robotwebtools.org/EventEmitter2/current/eventemitter2.js"></script>
        <link rel="shortcut icon" href="">

        <body>
            <h1>
                Turtle Bot Navigation
            </h1>
            <p>
                Communicate to turtle bot from the webpage
            </p>
            <script type="text/javascript">
                var ros = new ROSLIB.Ros({
                    url : "ws://localhost:8000/ws"
                });

                ros.on('connection', function() {
                console.log('Connected to websocket server.');
                });

                ros.on('error', function(error) {
                console.log('Error connecting to websocket server: ', error);
                });

                ros.on('close', function() {
                console.log('Connection to websocket server closed.');
                });

                // Publishing a Topic
                // ------------------

                var cmdVel = new ROSLIB.Topic({
                ros : ros,
                name : '/cmd_vel',
                messageType : 'geometry_msgs/Twist'
                });

                var twist = new ROSLIB.Message({
                linear : {
                x : 0.0,
                y : 0.0,
                z : 0.0
                },
                angular : {
                x : 0.0,
                y : 0.0,
                z : 0.0
                }
                });

                console.log("Publishing cmd_vel");
                cmdVel.publish(twist);

                var listener = new ROSLIB.Topic({
                  ros : ros,
                  name : '/listener',
                  messageType : 'std_msgs/String'
                });
            
                listener.subscribe(function(message) {
                  console.log('Received message on ' + listener.name + ': ' + message.data);
                  listener.unsubscribe();
              });

            </script>
        </body>
    </head>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

async def velocity(x=0):
    async with websockets.connect("ws://localhost:9090") as websocket:
        await websocket.send(json.dumps({"op": "subscribe","topic": "/odom"}))
        msg = await websocket.recv()
        print(msg)
        await websocket.send(json.dumps({"op": "publish","topic": "/cmd_vel","msg":convertVelToCmd_vel(x,0,0)}))


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    async with websockets.connect("ws://localhost:9090") as websocket_ros:
      while True:
          data = await websocket.receive_text()
          # asyncio.run(velocity(float(data)))
          await websocket_ros.send(json.dumps({"op": "subscribe","topic": "/odom"}))
          msg = await websocket_ros.recv()
          await websocket_ros.send(json.dumps({"op": "publish","topic": "/cmd_vel","msg":convertVelToCmd_vel(float(data),0,0)}))

          await websocket.send_text(f"Frwd velocity of robot is: {data}")
          await websocket.send_text(f"Frwd velocity of robot is: {msg}")



# asyncio.run(hello())
# msg1 = json.dumps({"op": "subscribe","topic": "/odom"})
# msg2 = json.load({"op": "subscribe","topic": "/odom"})

# print(msg1)
# print(msg2)

# json_string = '{ "1":"Red", "2":"Blue", "3":"Green"}'
# parsed_json = json.loads(json_string)
# print(parsed_json)