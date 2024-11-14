****Scalable Microservices Architecture for Real-Time Video Frame Analysis****

---Overview---

This project aims to create a scalable microservices-based system for real-time video analysis. The architecture leverages Python, FastAPI, OpenCV, and AWS S3 for video upload, processing, and storage. The solution includes separate services for video upload and segment removal to ensure modularity, scalability, and easier maintenance.

---Components---

Video Upload Service: Allows users to upload videos to an AWS S3 bucket.

Video Processing Service: Processes the uploaded video by removing a specified segment and re-uploads the modified version to AWS S3.

***Technologies Used***

FastAPI: For creating RESTful API endpoints.

Boto3: To interact with AWS S3 for uploading and downloading videos.

OpenCV: To perform video processing tasks, such as segment removal.

AWS S3: Cloud storage for storing original and modified videos.

-----Setup Instructions-----

Prerequisites

Python 3.7+

AWS Account with an S3 bucket created.

Environment Variables for AWS credentials set as follows:

export AWS_ACCESS_KEY_ID='your_access_key_id'
export AWS_SECRET_ACCESS_KEY='your_secret_access_key'
export AWS_DEFAULT_REGION='your_region'  

***Installation***

Install required dependencies:

pip install fastapi boto3 opencv-python uvicorn

Running the Services

Video Upload Service

Run the video upload service:

uvicorn video_upload_service:app --reload

The service will be available at http://127.0.0.1:8000/upload_video/.

Video Processing Service

Run the video processing service:

uvicorn video_processing_service:app --reload --port 8001

The service will be available at http://127.0.0.1:8001/remove_segment/.

API Endpoints

Video Upload Service

POST /upload_video/

Description: Upload a video to the AWS S3 bucket.

Request Parameter: Video file in multipart/form-data format.

Response: Success message and video name.

Video Processing Service

POST /remove_segment/

Description: Remove a specified segment from an uploaded video.

Request Body:

{
  "video_name": "your_video_filename.mp4",
  "start_time": "MM:SS",
  "end_time": "MM:SS"
}

Response: Success message, modified video name, and a downloadable link.



---Folder Structure---

<repository-folder>/
├── video_upload_service.py     # Handles video uploads
├── video_processing_service.py # Handles video processing
├── README.md                   # Project overview and setup guide
└── LISENSE.txt                 # Lisence Doc


License

This project is licensed under the MIT License.

