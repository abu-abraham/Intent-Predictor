
import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import zlib
from PIL import Image
from object_detection.detection.object_detector import ObjectDetector

HOST=''
PORT=8485

def saveImage(frames):
    im = Image.fromarray(np.uint8(frame))
    im.save('saved.png')

detector = ObjectDetector()
detector.start()
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind((HOST,PORT))
s.listen(10)
print('Socket now listening')


conn,addr=s.accept()

data = b""
payload_size = struct.calcsize(">L")


while True:
    while len(data) < payload_size:
        data += conn.recv(4096)

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    #saveImage(frame)
    print(detector.detect_objects(frame))
    
