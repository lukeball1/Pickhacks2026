import cloudinary
from config import IMG_API_KEY, IMG_API_SECRET, IMG_STORAGE_NAME

cloudinary.config(
    cloud_name=IMG_STORAGE_NAME,
    api_key=IMG_API_KEY,
    api_secret=IMG_API_SECRET,
)


def upload_image(image_path):
    result = cloudinary.uploader.upload(image_path)
    return result["secure_url"]
