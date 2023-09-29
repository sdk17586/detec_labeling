from PIL import Image
import os

# 원본 이미지 경로
image_folder = "/root/labe_ws/ob/data/drink"
# 리사이즈된 이미지 저장 경로
resize_folder = "/root/labe_ws/ob/resize_data/resize_drink"
os.makedirs(resize_folder, exist_ok=True)

# 원하는 크기로 리사이즈할 크기
desired_size = (500, 500)

image_files = [f for f in os.listdir(image_folder) if f.endswith(".jpg") or f.endswith(".png")]

for image_file in image_files:

    original_image_path = os.path.join(image_folder, image_file)
    resized_image_path = os.path.join(resize_folder, image_file)


    image = Image.open(original_image_path)

    image = image.resize(desired_size, Image.LANCZOS)
    image.save(resized_image_path)

print("이미지 리사이즈 및 저장 완료.")
