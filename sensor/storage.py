import cloudinary as cld
import cloudinary.uploader as upl
from config import IMG_API_KEY, IMG_API_SECRET, IMG_STORAGE_NAME

cld.config(
    cloud_name=IMG_STORAGE_NAME,
    api_key=IMG_API_KEY,
    api_secret=IMG_API_SECRET,
)


def upload_image(image_path):
    print("start")
    result = upl.upload(image_path)
    print("stop")
    return result["secure_url"]
