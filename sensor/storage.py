import cloudinary as cld
import cloudinary.uploader as upl
from config import IMG_API_KEY, IMG_API_SECRET, IMG_STORAGE_NAME

cld.config(
    cloud_name='duaqczxir',
    api_key='932599918752923',
    api_secret='4VxunUYPHFmtP1jaH0tcvPUyt7E',
)


def upload_image(image_path):
    result = upl.upload(image_path)
    return result["secure_url"]
