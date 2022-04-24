import os
import shutil

from deepface import DeepFace
import cv2
import numpy as np

from PIL import Image

import torchvision.transforms as T
import torchvision.transforms.functional as F


class SquarePad:
    def __call__(self, image):
        w, h = image.size
        max_wh = np.max([w, h])
        hp = int((max_wh - w) / 2)
        vp = int((max_wh - h) / 2)
        padding = (hp, vp, hp, vp)
        return F.pad(image, padding, 0, 'constant')

transform = T.Compose([
    SquarePad(),
    T.Resize(224)
])


def process_frames(frames_in, faces_out):
    for video in os.listdir(frames_in):
        frame_dir = os.path.join(frames_in, video)
        face_dir = os.path.join(faces_out, video)
        os.makedirs(face_dir, exist_ok=True)
        for frame in os.listdir(frame_dir):
            frame_path = os.path.join(frame_dir, frame)
            face_path = os.path.join(face_dir, frame)
            # if os.path.isfile(face_path):
            #     continue

            try:
                face = (DeepFace.detectFace(frame_path,
                                            detector_backend='retinaface',
                                            enforce_detection=True) * 255).astype(np.uint8)
                cv2.imwrite(face_path, cv2.cvtColor(face, cv2.COLOR_RGB2BGR))
            except:
                print('face detection failed for', frame_path, ', skipping')
                img = Image.open(frame_path)
                img = transform(img)
                assert (224, 224) == img.size
                img.save(face_path)
                img.show()

        print(video, 'done')


if __name__ == '__main__':
    frames_in = 'data/frame/'
    faces_out = 'data/face/'
    process_frames(frames_in, faces_out)
