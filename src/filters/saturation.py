import cv2

def apply_saturation(image, scale=1.5):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv[:, :, 1] = cv2.multiply(hsv[:, :, 1], scale)  # Saturation channel 조정
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
