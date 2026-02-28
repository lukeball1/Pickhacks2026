import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name="duaqczxir",
    api_key="932599918752923",
    api_secret="4VxunUYPHFmtP1jaH0tcvPUyt7E"
)

def upload_image(image_path):
    print("trying to upload")
    result = cloudinary.uploader.upload(image_path)
    print("uploaded")
    return result["secure_url"]