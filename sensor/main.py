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
            print("scanning...")
            frame = capture_frame(CAMERA_ID)

            # Save temporary image for inference
            temp_file = "temp.jpg"
            cv2.imwrite(temp_file, frame)
            result = detect_pothole(temp_file)

            detected, confidence, size = is_pothole_detected(result)
            if detected:
                print(f"[{time.strftime('%m/%d/%Y %H:%M:%S')}] pothole detected with confidence {confidence:.3f}\n")

                location = get_current_location()
                print("here02", temp_file)
                image_url = upload_image("temp.jpg")
                print("here03")
                road_info, coords = snap_point_to_road(
                    location["latitude"], location["longitude"]
                )
                print("here00")
                pothole_data = {
                    "location": {
                        "type": "Point",
                        "coordinates": [coords["lat"], coords["lon"]],
                    },
                    "confidence": confidence,
                    "size": size,
                    "image_url": image_url,
                    "vehicle_id": VEHICLE_ID,
                    "status": "unconfirmed",
                    "detection_date": time.strftime("%m/%d/%Y %H:%M")
                }
                print("here01")
                for k, v in road_info.items():
                    pothole_data[k] = v

                insert_or_update_pothole(collection, pothole_data, DUPLICATE_DISTANCE_M)

                print("Pothole reported to database.")

        except Exception as e:
            print("Error in main loop:", e)

        time.sleep(1)


if __name__ == "__main__":
    main_loop()
