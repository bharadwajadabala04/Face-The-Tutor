# detectors/head_pose.py
def is_head_down(shape):
    nose_tip_y = shape.part(30).y
    chin_y = shape.part(8).y
    delta = chin_y - nose_tip_y
    return delta < 15  # threshold for head-down posture
