import os
from PIL import Image

folder_path = r"G:\\My Drive\School\\01_Fall2024\\FinalProj\\assets\\towers\\references"
output_folder = r"G:\\My Drive\School\\01_Fall2024\\FinalProj\\assets\\towers"

for filename in os.listdir(folder_path):
    if filename.endswith("0.png"):
        img_path = os.path.join(folder_path, filename)
        x = 60
        with Image.open(img_path) as img:
            resized_img = img.resize((45, 45), Image.Resampling.LANCZOS) # 135x135 for 1920x1080, 150x150 for 2k monitor res for space images
            resized_img = resized_img.rotate(180, expand=True)
            resized_img.save(os.path.join(output_folder, filename))

    elif filename.endswith("1.png"):
        img_path = os.path.join(folder_path, filename)
        x = 65
        with Image.open(img_path) as img:
            resized_img = img.resize((x, x), Image.Resampling.LANCZOS) # 135x135 for 1920x1080, 150x150 for 2k monitor res for space images
            resized_img = resized_img.rotate(180, expand=True)
            resized_img.save(os.path.join(output_folder, filename))
    elif filename.endswith("2.png"):
        img_path = os.path.join(folder_path, filename)
        x = 70
        with Image.open(img_path) as img:
            resized_img = img.resize((x, x), Image.Resampling.LANCZOS) # 135x135 for 1920x1080, 150x150 for 2k monitor res for space images
            resized_img = resized_img.rotate(180, expand=True)
            resized_img.save(os.path.join(output_folder, filename))
    elif filename.endswith("3.png"):
        img_path = os.path.join(folder_path, filename)
        x = 75
        with Image.open(img_path) as img:
            resized_img = img.resize((x, x), Image.Resampling.LANCZOS) # 135x135 for 1920x1080, 150x150 for 2k monitor res for space images
            resized_img = resized_img.rotate(180, expand=True)
            resized_img.save(os.path.join(output_folder, filename))
    elif filename.endswith("4.png"):
        img_path = os.path.join(folder_path, filename)
        x = 80
        with Image.open(img_path) as img:
            resized_img = img.resize((x, x), Image.Resampling.LANCZOS) # 135x135 for 1920x1080, 150x150 for 2k monitor res for space images
            resized_img = resized_img.rotate(180, expand=True)
            resized_img.save(os.path.join(output_folder, filename))

print("done")