from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="http://localhost:9001",
    api_key="w8zz6jPett5K5OGjvfR3"
)

result2 = CLIENT.infer("hole.jpg", model_id="object-detection-bounding-box-ftfs5/1")

print("hole", result2)
