from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>ROS WEB</title>
    </head>
    <body>
        <iframe src="http://rtsp-simple-server-ip:8889/mystream" scrolling="no"></iframe>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)



#ffmpeg -f v4l2 -i /dev/video0 -pix_fmt yuv420p -c:v libx264 -preset ultrafast  -tune zerolatency -f rtsp rtsp://localhost:8554/mystream 