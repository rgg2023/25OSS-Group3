import cv2
import numpy as np
import mediapipe as mp

def apply_remove_person(image):
    """
    Detect and remove persons from the image using Mediapipe Selfie Segmentation.

    Parameters:
        image (numpy.ndarray): Input image in BGR format.

    Returns:
        numpy.ndarray: Image with persons removed and background filled.
    """
    # Initialize Mediapipe Selfie Segmentation
    mp_selfie_segmentation = mp.solutions.selfie_segmentation

    # Convert the image to RGB for Mediapipe
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Perform segmentation
    with mp_selfie_segmentation.SelfieSegmentation(model_selection=1) as segmentation:
        results = segmentation.process(rgb_image)

        # Create mask for detected persons
        mask = results.segmentation_mask > 0.5
        mask = mask.astype(np.uint8) * 255  # Convert to binary mask (0 or 255)

        # Invert the mask (person areas become white, background black)
        mask_inv = cv2.bitwise_not(mask)

        # Use inpainting to fill the person area with background
        inpainted_image = cv2.inpaint(image, mask, inpaintRadius=7, flags=cv2.INPAINT_TELEA)

        return inpainted_image


'''
가상환경에서 러스트가 인식이 안 됨.
import cv2
import numpy as np
import mediapipe as mp
from lama_cleaner.model_manager import ModelManager
from lama_cleaner.schema import Config, HDStrategy

# AI 기반 사람 제거 필터
def apply_remove_person(image):
    """
    Detect and remove persons from the image using Mediapipe Selfie Segmentation,
    then fill the area using LaMa (AI-based inpainting).

    Parameters:
        image (numpy.ndarray): Input image in BGR format.

    Returns:
        numpy.ndarray: Image with persons removed and area filled using AI inpainting.
    """
    # Step 1: Mediapipe를 사용해 사람을 감지
    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_selfie_segmentation.SelfieSegmentation(model_selection=1) as segmentation:
        results = segmentation.process(rgb_image)
        mask = (results.segmentation_mask > 0.5).astype(np.uint8) * 255  # 마스크 생성

    # Step 2: LaMa 모델 초기화
    model = ModelManager("lama")
    config = Config(
        hd_strategy=HDStrategy.CROP,
        hd_strategy_crop_margin=32,
        hd_strategy_crop_trigger_size=512,
        hd_strategy_resize_limit=2048,
    )

    # Step 3: AI 기반 인페인팅 실행
    inpainted_image = model(image, mask, config)
    return inpainted_image
'''