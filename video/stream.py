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
        <video width="640" height="480" controls>
            <source src="rtsp://localhost:8554/live" type="application/x-rtsp">
        </video>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)