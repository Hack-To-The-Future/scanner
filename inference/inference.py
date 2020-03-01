import json
from io import BytesIO
from multiprocessing import Process
import time

import numpy as np
from PIL import Image
from picamera import PiCamera
from websocket import create_connection

import tensorflow.keras  # noqa


class Inference(object):
    def __init__(self):
        super(Inference, self).__init__()
        np.set_printoptions(suppress=True)

        self.camera = PiCamera()
        self.camera.resolution = (244, 244)

        self.ws = None
        self.readlabels()
        self.model = tensorflow.keras.models.load_model('model/keras_model.h5')
        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        self.ws = create_connection("ws://0.0.0.0:8000/ws", sslopt={"check_hostname": False})


    def readlabels(self):
        fn = 'model/labels.txt'

        with open(fn, 'r') as f:
            lines = f.readlines()

        self.labels = {}
        self.item_count = {}
        self.label_last_seen = {}
        for line in lines:
            tokens = line.split()
            label = ' '.join(tokens[1:]).rstrip()
            if label == 'None':
                label = None
            self.labels[int(tokens[0])] = label

        for ind, label in self.labels.items():
            if label is not None:
                self.item_count[label] = 0
                self.label_last_seen[label] = time.time()

    def __del__(self):
        if self.ws is not None:
            self.ws.close()

    def run(self):
        
        while True:
            stream = BytesIO()
            self.camera.capture(stream, format='jpeg', resize=(224, 224))
            stream.seek(0)

            image_array = np.asarray(Image.open(stream))
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
            self.data[0] = normalized_image_array
            prediction = self.model.predict(self.data)[0]

            pred_val = np.max(prediction)
            label = None
            if pred_val > 0.8:
                label = self.labels[int(np.argmax(prediction))]
            
            now = time.time()
            if label is not None and int(now - self.label_last_seen[label]) > 5:
                print(label)
                self.item_count[label] += 1
                self.label_last_seen[label] = now
                self.ws.send(json.dumps({
                    "prediction": self.item_count
                }))


if __name__ == '__main__':
    inf_proc = Inference()
    inf_proc.run()
