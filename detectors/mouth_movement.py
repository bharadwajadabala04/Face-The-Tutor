from scipy.spatial import distance

def mouth_open_ratio(shape):
    A = distance.euclidean((shape.part(62).x, shape.part(62).y), (shape.part(66).x, shape.part(66).y))  # vertical
    B = distance.euclidean((shape.part(60).x, shape.part(60).y), (shape.part(64).x, shape.part(64).y))  # horizontal
    return A / B if B != 0 else 0

def is_talking(shape):
    ratio = mouth_open_ratio(shape)
    return ratio > 0.6  # You can tune this to 0.5–0.65
