import cv2
import numpy as np
import mediapipe as mp


def apply_portrait_mode(image):
    """
    Blur all areas except detected persons (body) in the image.
    Handles single and multiple persons differently.

    Parameters:
        image (numpy.ndarray): Input image in BGR format.

    Returns:
        numpy.ndarray: Image with non-person areas blurred.
    """
    # Initialize Mediapipe Pose for multi-person detection
    mp_pose = mp.solutions.pose
    mp_selfie_segmentation = mp.solutions.selfie_segmentation

    # Convert the image to RGB for Mediapipe
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Step 1: Try single person detection using Selfie Segmentation
    segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)
    results_segmentation = segmentation.process(rgb_image)

    # Check if a single person is detected with a confident mask
    condition = results_segmentation.segmentation_mask > 0.5
    if np.any(condition):  # If a single person mask is detected
        mask = np.where(condition, 255, 0).astype(np.uint8)
        mask_inv = cv2.bitwise_not(mask)

        # Blur the entire image
        blurred_image = cv2.GaussianBlur(image, (51, 51), 0)

        # Combine the original image and blurred image using the masks
        person_areas = cv2.bitwise_and(image, image, mask=mask)
        non_person_areas = cv2.bitwise_and(blurred_image, blurred_image, mask=mask_inv)

        segmentation.close()
        return cv2.add(person_areas, non_person_areas)

    # Step 2: If single person is not detected, use Pose Detection for multiple persons
    with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
        results_pose = pose.process(rgb_image)

        # Generate a blank mask for multiple people
        height, width, _ = image.shape
        multi_person_mask = np.zeros((height, width), dtype=np.uint8)

        # If pose landmarks are detected
        if results_pose.pose_landmarks:
            for landmark in results_pose.pose_landmarks.landmark:
                x = int(landmark.x * width)
                y = int(landmark.y * height)
                cv2.circle(multi_person_mask, (x, y), 50, 255, thickness=-1)

        # Invert the mask (non-person areas become white)
        mask_inv = cv2.bitwise_not(multi_person_mask)

        # Blur the entire image
        blurred_image = cv2.GaussianBlur(image, (51, 51), 0)

        # Combine the original image and blurred image using the masks
        person_areas = cv2.bitwise_and(image, image, mask=multi_person_mask)
        non_person_areas = cv2.bitwise_and(blurred_image, blurred_image, mask=mask_inv)

        return cv2.add(person_areas, non_person_areas)


# Example usage
if __name__ == "__main__":
    # Load an image
    image = cv2.imread("test_image.jpg")

    # Apply portrait mode
    result_image = apply_portrait_mode(image)

    # Display the result
    cv2.imshow("Portrait Mode", result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
