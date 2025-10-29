import cv2

def apply_edge_detection(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)  # Canny Edge Detection
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)  # Convert to 3-channel
