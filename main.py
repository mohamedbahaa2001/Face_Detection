import time
import cv2
import numpy as np
import face_recognition
import os
import ctypes
from plyer import notification

path = 'images'
images = []
classNames = []
myList = os.listdir(path)
name = ''
print('my list',myList)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print('class name',classNames)


def findencoding(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


encodeListknown = findencoding(images)
print('length',len(encodeListknown))

cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    imgs = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)
    facesCurFrame = face_recognition.face_locations(imgs)
    encodeCurFrame = face_recognition.face_encodings(imgs, facesCurFrame)
    print('facesCurFrame',facesCurFrame)
    if len(encodeCurFrame) == 0:
        notification.notify(title = "Admin not Detected",
        message = "Computer will lock in 10 seconds",
        timeout = 10)
        print('no face detected the computer will lock in 10 seconds')
        time.sleep(10)
        ctypes.windll.user32.LockWorkStation()
        break
    for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListknown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListknown, encodeFace)
        print(faceDis)
        matcheIndex = np.argmin(faceDis)
        if matches[matcheIndex]:
            name = classNames[matcheIndex].upper()
            print(name)

        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


    cv2.imshow('camera', img)

    cv2.waitKey(1)
