#!/usr/bin/python

import uvicorn
import cv2
import numpy as np
from fastapi import FastAPI
from fastapi.responses import StreamingResponse


FRAME_WIDTH = 640
FRAME_HEIGHT = 480

server = FastAPI()


def _video_streamer():
    while True:
        simulated_frame = np.random.randint(0, 256, (FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)
        _, jpg_frame = cv2.imencode('.jpg', simulated_frame)
        yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + bytearray(jpg_frame) + b'\r\n'


@server.get("/")
def get_root():
    return "Simulated Webcam Streaming"


@server.get("/video_feed_1")
def video_feed():
    return StreamingResponse(_video_streamer(), media_type='multipart/x-mixed-replace;boundary=frame')

@server.get("/video_feed_2")
def video_feed():
    return StreamingResponse(_video_streamer(), media_type='multipart/x-mixed-replace;boundary=frame')

@server.get("/video_feed_3")
def video_feed():
    return StreamingResponse(_video_streamer(), media_type='multipart/x-mixed-replace;boundary=frame')


if __name__ == "__main__":
    uvicorn.run(server, host="0.0.0.0", port=8000)
