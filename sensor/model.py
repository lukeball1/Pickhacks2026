from inference_sdk import InferenceHTTPClient, InferenceConfiguration
from config import API_URL, API_KEY, MODEL_ID

CONFIGURATION = InferenceConfiguration(
    confidence_threshold=0.75
)

CLIENT = InferenceHTTPClient(api_url=API_URL, api_key=API_KEY)

def detect_pothole(image_path):
    """
    Send image to inference server.
    Returns raw result dictionary.
    """
    CLIENT.configure(CONFIGURATION)
    return CLIENT.infer(image_path, model_id=MODEL_ID)


def is_pothole_detected(result):
    """
    Parse inference result.

    Returns:
        is_pothole (bool)
        confidence (float)
        size (dict)
    """

    predictions = result.get("predictions", [])

    pothole_predictions = [p for p in predictions if p.get("class") == "Potholes"]

    if not pothole_predictions:
        return False, 0.0, {}

    # Choose highest confidence detection
    best = max(pothole_predictions, key=lambda x: x.get("confidence", 0))

    confidence = best.get("confidence", 0.0)

    size = {
        "width_cm": best.get("width"),
        "height_cm": best.get("height"),
    }

    return True, confidence, size
