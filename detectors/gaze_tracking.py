# detectors/gaze_tracking.py
def is_watching_away(shape):
    nose_x = shape.part(30).x
    left_face = shape.part(0).x
    right_face = shape.part(16).x
    face_center = (left_face + right_face) // 2

    offset = abs(nose_x - face_center)
    if offset > 35:  # threshold, tune if needed
        return True
    return False
