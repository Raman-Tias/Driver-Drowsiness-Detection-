import cv2 
import imutils 
from imutils import face_utils 
import dlib 
from scipy.spatial import distance 
from pygame import mixer 
mixer.init() 
mixer.music.load("music.wav") 
def eye_aspect_ratio(eye): 
A = distance.euclidean(eye[1], eye[5]) 
B = distance.euclidean(eye[2], eye[4]) 
C = distance.euclidean(eye[0], eye[3]) 
ear = (A + B) / (2.0 * C) 
return ear 
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS['left_eye'] 
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS['right_eye'] 
detect = dlib.get_frontal_face_detector() 
predict = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat") 
cap = cv2.VideoCapture(0) 
thresh = 0.3   
frame_check = 20   
flag = 0 
while True: 
    ret, frame = cap.read() 
    frame = imutils.resize(frame, width=450)  # Resize the frame for faster 
processing 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale for 
dlib 
    subjects = detect(gray, 0)  # Detect faces 
 
    for subject in subjects: 
        shape = predict(gray, subject) 
        shape = face_utils.shape_to_np(shape) 
 
        leftEye = shape[lStart:lEnd] 
        rightEye = shape[rStart:rEnd] 
 
        leftEAR = eye_aspect_ratio(leftEye) 
        rightEAR = eye_aspect_ratio(rightEye) 
        ear = (leftEAR + rightEAR) / 2.0 
        leftEyeHull = cv2.convexHull(leftEye) 
        rightEyeHull = cv2.convexHull(rightEye) 
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1) 
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1) 
 
        if ear < thresh: 
            flag += 1 
 print(flag) 
            if flag >= frame_check: 
                cv2.putText(frame, "!!!!!!!!! Alert  Wake up !!!!!!!!", (10, 30), 
cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2) 
                cv2.putText(frame, "!!!!!!!!! Alert Wake up !!!!!!!!", (10, 325), 
cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2) 
                mixer.music.play()  # Play the alert sound 
        else: 
            flag = 0   
    cv2.imshow("Frame", frame) 
 
    if cv2.waitKey(1) & 0xFF == ord("q"): 
        break 
cv2.destroyAllWindows() 
cap.release()