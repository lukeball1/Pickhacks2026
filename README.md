## Resources
[Google Drive]('https://drive.google.com/drive/folders/14prWPCflTm6go9ODh0x4hmkm0kVSvxpI?usp=sharing')

Pothole Classification Model:
* [GitHub](https://github.com/mounishvatti/pothole_detection_yolov8)
* [Roboflow cloud model instance](https://universe.roboflow.com/hiteshram/object-detection-bounding-box-ftfs5/model/1)
* [Inference Client Documentation](https://inference.roboflow.com/inference_helpers/inference_sdk/)

# Sensor Setup

## 1. Clone this Repository
Clone this repository to your device.

## 2. Install Docker
Follow the instructions [here](https://docs.docker.com/desktop/) to install Docker Desktop on your device. 

## 3. Initialize Python Virual Environment
This will allow you to locally run the simple ML model. Enter the command below:
`python3 -m venv .venv` 

## 4. Download the Requirements.txt libraries
Inside your virtual environment, run `pip install -r requirements.txt`

## Model Local Server Setup
1. Download Docker Engine and ensure the daemon is running
2. Go to Code Snippets section of the cloud model on roboflow
3. Follow Inference CLI installation instructions in On Devie tab*\
***important:** If using the model through the command line and not Python, the command in Roboflow is outdated. Use the following syntax instead: `inference infer -i 'hole.jpg' --api-key w8zz6jPett5K5OGjvfR3 --model_id object-detection-bounding-box-ftfs5/1`
4. Use the inference client documentation to send requests to your local inference server via python

## To run the Backend FLASK server
1. Open a new terminal and navigate to the server directory. 
2. Run the command `flask --app app run`. This will startup the flask server
3. The server will run on port 5000

## To run the Frontend server 
1. Make sure you have Next.js installed
2. Open a new terminal and navigate to the client directory.
3. Run the command `npm run dev`
4. The frontend server will be running locally on port 5173.