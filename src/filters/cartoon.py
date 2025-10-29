# 딥러닝 기반으로 변경하는 게 좋을 듯.
import cv2

def apply_cartoon(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply median blur
    gray_blurred = cv2.medianBlur(gray, 7)

    # Detect edges using adaptive thresholding
    edges = cv2.adaptiveThreshold(gray_blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    # Reduce noise and create a cartoon effect
    color = cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)

    # Combine edges and color
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    return cartoon
