Member Names:
Deepak Reddy Nayani
Karthik Aravapalli
Nikhil Chandra Nirukonda

Bucket Names:
input bucket name : ndk-proj2
output bucket name : ndk-proj2output

DB table name : ndk-proj2-table

Download and install AWS CLI
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

Go to terminal, and run “aws configure”, then type in the AWS_ACCESS_KEY, AWS_SECRET_KEY & REGION
Git Clone the repository and cd into it.

AWS_REGION = "us-east-1"
aws_access_key_id = "AAAAAAAAAAAAAAAAA"
aws_secret_access_key = "BBBBBBBBBBBBBBBB"

Make the following changes (if using the TAs code)
In Dockerfile, add a line “COPY encoding /home/app/”
In requirements.txt, change ffmpeg to python-ffmpeg

Download and install Docker and Docker Desktop for deploying the image.
Run the following commands:
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 458362110587.dkr.ecr.us-east-1.amazonaws.com
docker build -t proj2-docker-lambda .
docker tag proj2-docker-lambda:latest 458362110587.dkr.ecr.us-east-1.amazonaws.com/proj2-docker-lambda:latest
docker push 458362110587.dkr.ecr.us-east-1.amazonaws.com/proj2-docker-lambda:latest

Run python3 uploadDB.py (should not be required as the table is already populated)
Run python3 workload.py to upload the videos in the test folder into the S3 bucket.
