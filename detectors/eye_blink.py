# detectors/eye_blink.py
from scipy.spatial import distance
from config import BLINK_CONSEC_FRAMES

BLINK_COUNTER = 0
TOTAL_BLINKS = 0
EAR_THRESHOLD = 0.21  # Typically used threshold

def eye_aspect_ratio(eye):
    A = distance.euclidean((eye[1].x, eye[1].y), (eye[5].x, eye[5].y))
    B = distance.euclidean((eye[2].x, eye[2].y), (eye[4].x, eye[4].y))
    C = distance.euclidean((eye[0].x, eye[0].y), (eye[3].x, eye[3].y))
    return (A + B) / (2.0 * C)

def is_blinking(shape):
    global BLINK_COUNTER, TOTAL_BLINKS

    left_eye = [shape.part(i) for i in range(36, 42)]
    right_eye = [shape.part(i) for i in range(42, 48)]

    ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2.0

    if ear < EAR_THRESHOLD:
        BLINK_COUNTER += 1
    else:
        if BLINK_COUNTER >= BLINK_CONSEC_FRAMES:
            TOTAL_BLINKS += 1
            BLINK_COUNTER = 0
            return True
        BLINK_COUNTER = 0

    return False
