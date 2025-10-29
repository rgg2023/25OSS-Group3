import cv2
import numpy as np

def apply_grayscale(image):
    if image is None or not isinstance(image, np.ndarray):  # 들여쓰기 수정
        raise ValueError("Invalid image.")
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return grayscale_image
