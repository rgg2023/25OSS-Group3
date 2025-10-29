from PIL import Image
import os
from datetime import datetime


def create_gif(image_folder, output_gif_path, duration=600):
    image_files = [f"{i}.png" for i in range(1, 25)]  # 1.png부터 24.png까지 예시 (필요에 따라 범위 조정)

    images = []
    max_width = 0
    max_height = 0

    # 첫 번째 이미지를 확인하여 최대 크기를 계산
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        if os.path.exists(image_path):
            image = Image.open(image_path)
            # 가장 큰 이미지의 크기
            max_width = max(max_width, image.width)
            max_height = max(max_height, image.height)
        else:
            print(f"파일이 존재하지 않습니다: {image_path}")
            return

    # 각 이미지를 열고 크기를 맞추고, 작은 이미지는 중앙에 배치
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        if os.path.exists(image_path):
            image = Image.open(image_path)

            # 이미지를 최대 크기에 맞춰서 크기 변경
            new_image = Image.new("RGBA", (max_width, max_height), (255, 255, 255, 0))  # 배경은 투명

            # 원본 이미지를 중앙에 배치
            offset = ((max_width - image.width) // 2, (max_height - image.height) // 2)
            new_image.paste(image, offset)
            images.append(new_image)
        else:
            print(f"파일이 존재하지 않습니다: {image_path}")
            return

    # 첫 번째 이미지에서 GIF로 저장
    images[0].save(output_gif_path, save_all=True, append_images=images[1:], duration=duration, loop=0)
    print(f"GIF 파일이 저장되었습니다: {output_gif_path}")


# 사용 예시
if __name__ == "__main__":
    # 현재 스크립트가 위치한 폴더 경로
    current_folder = os.path.dirname(os.path.realpath(__file__))

    # 현재 날짜와 시간을 추가한 파일 이름 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # "YYYYMMDD_HHMMSS" 형식
    output_gif_path = os.path.join(current_folder, f"output_{timestamp}.gif")

    create_gif(current_folder, output_gif_path)
