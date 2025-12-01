import cv2
import numpy as np
from transformers import AutoModelForImageSegmentation, AutoProcessor
import torch


class PersonRemover:
    def __init__(self):
        # HuggingFace의 RemBG 최고 성능 모델
        model_name = "briaai/RMBG-1.4"

        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = AutoModelForImageSegmentation.from_pretrained(model_name)

    def remove_person(self, image):
        """
        인물 제거 + 자연스러운 배경 복원 (RMBG 모델 기반)
        image: (numpy.ndarray), BGR 이미지
        return: 사람 제거 후의 이미지
        """

        # BGR → RGB
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 모델 입력
        inputs = self.processor(images=rgb, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model(**inputs)

        # 마스크 추출
        mask = outputs.pred_masks.squeeze().cpu().numpy()  # float mask

        # 0~1 → 0 또는 255
        mask = (mask > 0.5).astype(np.uint8) * 255

        # OpenCV inpaint로 사람 영역 제거 후 자연스럽게 보정
        inpainted = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)

        return inpainted


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
