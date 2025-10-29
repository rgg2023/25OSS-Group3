import cv2
import mediapipe as mp
import numpy as np


def apply_mosaic_to_faces(image, scale=5):
    """
    Apply a strong mosaic filter to detected faces in an image using Mediapipe Face Detection.

    Parameters:
        image (numpy.ndarray): Input image in BGR format.
        scale (int): The scale factor for the mosaic effect (fixed to a strong value).

    Returns:
        numpy.ndarray: Image with strong mosaic applied to detected faces.
    """
    if not isinstance(image, np.ndarray):
        raise TypeError("Input image must be a numpy.ndarray.")

    # Initialize Mediapipe Face Detection
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.7)

    # Convert the image to RGB (Mediapipe requires RGB format)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Perform face detection
    results = face_detection.process(rgb_image)

    # If faces are detected, apply mosaic
    if results.detections:
        for detection in results.detections:
            try:
                # Get bounding box coordinates
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = image.shape
                x = int(bboxC.xmin * iw)
                y = int(bboxC.ymin * ih)
                w = int(bboxC.width * iw)
                h = int(bboxC.height * ih)

                # Ensure coordinates are within image bounds
                x, y = max(0, x), max(0, y)
                x2, y2 = min(iw, x + w), min(ih, y + h)

                # Extract the face region
                face_region = image[y:y2, x:x2]

                # Apply strong mosaic to the face region
                if face_region.size > 0:  # Avoid processing empty regions
                    # Force strong mosaic with a fixed low-resolution resize
                    face_region = cv2.resize(face_region, (10, 10), interpolation=cv2.INTER_LINEAR)
                    face_region = cv2.resize(face_region, (x2 - x, y2 - y), interpolation=cv2.INTER_NEAREST)

                    # Replace the face region with the mosaic version
                    image[y:y2, x:x2] = face_region
            except Exception as e:
                print(f"Error applying mosaic to a face: {e}")

    # Release Mediapipe resources
    face_detection.close()

    return image
