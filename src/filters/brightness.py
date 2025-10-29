import cv2

def apply_brightness(image, value=50):
    return cv2.convertScaleAbs(image, alpha=1, beta=value)  # beta는 밝기 조정
