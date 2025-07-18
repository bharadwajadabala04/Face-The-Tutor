from scipy.spatial import distance
from config import EAR_THRESHOLD, DROWSY_FRAMES

COUNTER = 0

def eye_aspect_ratio(eye):
    A = distance.euclidean((eye[1].x, eye[1].y), (eye[5].x, eye[5].y))
    B = distance.euclidean((eye[2].x, eye[2].y), (eye[4].x, eye[4].y))
    C = distance.euclidean((eye[0].x, eye[0].y), (eye[3].x, eye[3].y))
    return (A + B) / (2.0 * C)

def is_drowsy(shape):
    global COUNTER

    left_eye = [shape.part(i) for i in range(36, 42)]
    right_eye = [shape.part(i) for i in range(42, 48)]

    ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2.0

    if ear < EAR_THRESHOLD:
        COUNTER += 1
        if COUNTER >= DROWSY_FRAMES:
            COUNTER = 0
            return True
    else:
        COUNTER = 0

    return False
