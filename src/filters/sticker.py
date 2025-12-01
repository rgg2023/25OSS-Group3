import cv2
import mediapipe as mp
import numpy as np
import os
import requests
from io import BytesIO
from PIL import Image


def load_sticker():
    sticker_url = "https://upload.wikimedia.org/wikipedia/commons/d/d7/Discord_cat_neutral.png"
    sticker_path = "discord_cat_neutral.png"

    # 파일이 없으면 다운로드
    if not os.path.exists(sticker_path):
        print("Downloading sticker from internet...")
        try:
            response = requests.get(sticker_url, timeout=10)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            img.save(sticker_path)
        except Exception as e:
            raise RuntimeError(f"Failed to download sticker: {e}")

    sticker = cv2.imread(sticker_path, cv2.IMREAD_UNCHANGED)
    if sticker is None:
        raise RuntimeError("Failed to load the sticker image.")

    return sticker


def apply_sticker(image):
    sticker = load_sticker()

    # Mediapipe Face Detection
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.7)

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb)

    if results.detections:
        for detection in results.detections:
            ih, iw, _ = image.shape
            bbox = detection.location_data.relative_bounding_box

            x = int(bbox.xmin * iw)
            y = int(bbox.ymin * ih)
            w = int(bbox.width * iw)
            h = int(bbox.height * ih)

            # 스티커 크기 조정
            sticker_width = w
            sticker_height = int(sticker.shape[0] * (sticker_width / sticker.shape[1]))
            resized = cv2.resize(sticker, (sticker_width, sticker_height))

            # 오프셋 계산
            x_offset = x + w//2 - sticker_width//2
            y_offset = y + h//2 - sticker_height//2

            # 범위 보정
            x1, y1 = max(0, x_offset), max(0, y_offset)
            x2 = min(iw, x1 + sticker_width)
            y2 = min(ih, y1 + sticker_height)

            sticker_crop = resized[(y1 - y_offset):(y2 - y_offset), (x1 - x_offset):(x2 - x_offset)]
            alpha = sticker_crop[:, :, 3] / 255.0
            alpha_inv = 1 - alpha

            # 스티커 합성 (Alpha blending)
            for c in range(3):
                image[y1:y2, x1:x2, c] = alpha * sticker_crop[:, :, c] + alpha_inv * image[y1:y2, x1:x2, c]

    face_detection.close()
    return image





"""
import cv2
import mediapipe as mp
import numpy as np
import os
import urllib.request


def apply_sticker(image):
    
    Mediapipe를 사용하여 얼굴을 인식하고 각 얼굴 위에 스티커를 배치합니다.
    스티커는 얼굴의 중심에 배치됩니다.
    사용 후 다운로드된 스티커 이미지를 자동으로 삭제합니다.

    Parameters:
        image (numpy.ndarray): Input image in BGR format.

    Returns:
        numpy.ndarray: Image with stickers applied to detected faces.
    """
    # 스티커 이미지 경로 설정
    sticker_path = os.path.join(os.getcwd(), "discord_cat_neutral.png")

    # 스티커 파일이 없으면 다운로드
    """
    if not os.path.exists(sticker_path):
        print("Sticker file not found locally. Downloading the Discord Cat Neutral image...")
        sticker_url = "https://upload.wikimedia.org/wikipedia/commons/d/d7/Discord_cat_neutral.png"
        try:
            urllib.request.urlretrieve(sticker_url, sticker_path)
        except Exception as e:
            raise RuntimeError(f"Failed to download the sticker image: {e}")

    # 스티커 이미지 로드
    sticker = cv2.imread(sticker_path, cv2.IMREAD_UNCHANGED)
    if sticker is None:
        raise FileNotFoundError("Sticker image not found.")

    # Mediapipe Face Detection 초기화
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.7)

    # 이미지를 RGB로 변환 (Mediapipe는 RGB 이미지 사용)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 얼굴 탐지
    results = face_detection.process(rgb_image)

    # 얼굴이 감지된 경우
    if results.detections:
        for detection in results.detections:
            try:
                # Mediapipe의 bounding box 정보를 가져옴
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = image.shape
                x = int(bboxC.xmin * iw)
                y = int(bboxC.ymin * ih)
                w = int(bboxC.width * iw)
                h = int(bboxC.height * ih)

                # 얼굴 중심 좌표 계산
                face_center_x = x + w // 2
                face_center_y = y + h // 2

                # 스티커 크기 조정
                sticker_width = w
                sticker_height = int(sticker.shape[0] * (sticker_width / sticker.shape[1]))
                resized_sticker = cv2.resize(sticker, (sticker_width, sticker_height), interpolation=cv2.INTER_AREA)

                # 스티커를 얼굴 중심에 배치
                x_offset = face_center_x - sticker_width // 2
                y_offset = face_center_y - sticker_height // 2

                # 스티커를 얼굴 위에 완전히 덮도록 배치
                for y_sticker in range(resized_sticker.shape[0]):
                    for x_sticker in range(resized_sticker.shape[1]):
                        if resized_sticker[y_sticker, x_sticker, 3] > 0:  # 투명 픽셀 확인
                            # 이미지 범위 초과 방지
                            if 0 <= (y_offset + y_sticker) < image.shape[0] and 0 <= (x_offset + x_sticker) < image.shape[1]:
                                # 스티커 픽셀로 얼굴을 완전히 덮음
                                image[y_offset + y_sticker, x_offset + x_sticker] = resized_sticker[y_sticker, x_sticker, :3]

            except Exception as e:
                print(f"Error applying sticker to a face: {e}")

    # Mediapipe 리소스 해제
    face_detection.close()

    # 다운로드된 스티커 파일 삭제
    if os.path.exists(sticker_path):
        try:
            os.remove(sticker_path)
            print(f"Deleted sticker file: {sticker_path}")
        except Exception as e:
            print(f"Error deleting sticker file: {e}")

    return image
"""
