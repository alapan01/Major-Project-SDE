from fastapi import FastAPI
from pydantic import BaseModel
import boto3
from botocore.exceptions import NoCredentialsError
import os
import cv2
import tempfile

app = FastAPI()

# AWS S3 setup
AWS_ACCESS_KEY = os.getenv('AKIAS66UDGOWUOLQL27S')
AWS_SECRET_KEY = os.getenv('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')
AWS_REGION = os.getenv('us-east-1')
AWS_BUCKET_NAME = 'sdemajorproject'  

s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name=AWS_REGION)

class VideoSegmentRequest(BaseModel):
    video_name: str
    start_time: str  # Format: "MM:SS"
    end_time: str    

@app.post("/remove_segment/")
async def remove_segment(request: VideoSegmentRequest):
    """
    Endpoint to specify the segment to remove from the uploaded video.
    """
    try:
        # Download the video from S3
        with tempfile.NamedTemporaryFile(delete=False) as temp_video_file:
            s3_client.download_fileobj(AWS_BUCKET_NAME, request.video_name, temp_video_file)
            temp_video_file_path = temp_video_file.name

        # Process the video 
        start_min, start_sec = map(int, request.start_time.split(":"))
        end_min, end_sec = map(int, request.end_time.split(":"))
        start_frame = (start_min * 60 + start_sec) * 30  # Assuming 30 FPS
        end_frame = (end_min * 60 + end_sec) * 30

        cap = cv2.VideoCapture(temp_video_file_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        # Create a temp file for the output video
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_output_file:
            temp_output_path = temp_output_file.name

        out = cv2.VideoWriter(temp_output_path, fourcc, fps, (width, height))

        current_frame = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Write frames that are not within the segment to be removed
            if current_frame < start_frame or current_frame > end_frame:
                out.write(frame)

            current_frame += 1

        cap.release()
        out.release()

        # Upload the modified video back to S3
        modified_video_name = f"modified_{request.video_name}"
        with open(temp_output_path, "rb") as modified_file:
            s3_client.upload_fileobj(modified_file, AWS_BUCKET_NAME, modified_video_name)

        # Generate a presigned URL for the modified video
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': AWS_BUCKET_NAME, 'Key': modified_video_name},
            ExpiresIn=3600  # expire time
        )

        
        os.remove(temp_video_file_path)
        os.remove(temp_output_path)

        return {
            "message": "Segment removed successfully",
            "modified_video_name": modified_video_name,
            "download_url": presigned_url
        }

    except NoCredentialsError:
        return {"error": "Credentials not available"}
    except Exception as e:
        return {"error": str(e)}
