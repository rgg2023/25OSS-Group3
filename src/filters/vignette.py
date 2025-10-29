import numpy as np
import cv2

def apply_vignette(image, scale=1.5):
    rows, cols = image.shape[:2]
    kernel_x = cv2.getGaussianKernel(cols, cols / scale)
    kernel_y = cv2.getGaussianKernel(rows, rows / scale)
    kernel = kernel_y * kernel_x.T
    mask = kernel / kernel.max()
    vignette = image * mask[..., np.newaxis]
    return np.clip(vignette, 0, 255).astype(np.uint8)
