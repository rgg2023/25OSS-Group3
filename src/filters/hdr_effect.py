import cv2

def apply_hdr_effect(image):
    return cv2.detailEnhance(image, sigma_s=10, sigma_r=0.15)
