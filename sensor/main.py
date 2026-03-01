import time
import cv2

from camera import capture_frame
from model import detect_pothole, is_pothole_detected
from db import connect_db, insert_or_update_pothole
from utils import get_current_location
from storage import upload_image
from config import CAMERA_ID, VEHICLE_ID, DUPLICATE_DISTANCE_M
from pickhacksroads import snap_point_to_road


def main_loop():
    collection = connect_db()

    while True:
        # time.sleep(1)
        try:
            print("capturing")
            frame = capture_frame(CAMERA_ID)

            # Save temporary image for inference
            temp_file = "temp.jpg"
            cv2.imwrite(temp_file, frame)
            print("written")
            result = detect_pothole(temp_file)

            detected, confidence, size = is_pothole_detected(result)
            print("analyzed.")
            if detected:
                print(f"Pothole detected with confidence {confidence:.3f}")

                location = get_current_location()

                filename = f"{VEHICLE_ID}_{int(time.time())}.jpg"
                image_url = upload_image(temp_file)
                road_info, coords = snap_point_to_road(
                    location["latitude"], location["longitude"]
                )
                pothole_data = {
                    "location": {
                        "type": "Point",
                        "coordinates": [coords["lat"], coords["lon"]],
                    },
                    "confidence": confidence,
                    "size": size,
                    "image_url": image_url,
                    "vehicle_id": VEHICLE_ID,
                    "status": "open",
                    "first_detected_at": time.time(),
                    "last_updated_at": time.time(),
                }
                for k, v in road_info.items():
                    pothole_data[k] = v

                insert_or_update_pothole(collection, pothole_data, DUPLICATE_DISTANCE_M)

                print("Pothole reported to database.")

        except Exception as e:
            print("Error in main loop:", e)

        time.sleep(1)


if __name__ == "__main__":
    main_loop()
