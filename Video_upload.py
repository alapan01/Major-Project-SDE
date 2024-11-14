from fastapi import FastAPI, UploadFile, File
import boto3
from botocore.exceptions import NoCredentialsError
import os

app = FastAPI()

# AWS S3 setup
AWS_ACCESS_KEY = os.getenv('...')
AWS_SECRET_KEY = os.getenv('...')
AWS_REGION = os.getenv('...')
AWS_BUCKET_NAME = '...'  

s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name=AWS_REGION)

@app.post("/upload_video/")
async def upload_video(file: UploadFile = File(...)):
    
    try:
        s3_client.upload_fileobj(file.file, AWS_BUCKET_NAME, file.filename)
        return {"message": "Video uploaded successfully", "video_name": file.filename}
    except NoCredentialsError:
        return {"error": "Credentials not available"}
    except Exception as e:
        return {"error": str(e)}
