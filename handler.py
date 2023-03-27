import boto3
import os
import face_recognition
import pickle
import ffmpeg
import json
import shutil
import csv
import time
from boto3.dynamodb.conditions import Key

#input_bucket = "ndk-proj2"
output_bucket = "ndk-proj2output"

AWS_REGION = "us-east-1"
aws_access_key_id = "AAAAAAAAAAAAAAAAAAAAAAAAAAA" #Enter appropriate access and secret keys
aws_secret_access_key = "BBBBBBBBBBBBBBBBBB"


# Function to read the 'encoding' file
def open_encoding(filename):
	file = open(filename, "rb")
	data = pickle.load(file)
	file.close()
	return data

def face_recognition_handler(event, context):
	
	print("Hello, Program entry point")

	###########################CLEAN-UP###################################
	if not os.path.exists("/tmp"):
		print("tmp does not exist and is being created")
		os.mkdir("/tmp")
	else:
		print("tmp already present")
	print("All the files present inside tmp")
	print(os.listdir("/tmp"))	

	if os.path.exists("/tmp/test_frames"):
		shutil.rmtree("/tmp/test_frames")
		print("Deleted the test_frames folder and the contents inside of it")

	for item in os.listdir("/tmp"):
		item_path = os.path.join("/tmp", item)
		if os.path.isfile(item_path):
			os.remove(item_path)
	##########################################################################
	
	#Parsing event to get bucket and file name
	print("Checking event")
	print(event)
	bucket_name = event['Records'][0]['s3']['bucket']['name']
	video_name = event['Records'][0]['s3']['object']['key']

	#Downloading videos from s3 into lambda
	getVideosfromS3(bucket_name, video_name)
	time.sleep(5)

	#Create a folder to store the frames in
	frame_directory = "/tmp/test_frames"
	if not os.path.exists(frame_directory):
		os.makedirs(frame_directory)
		print("Folder to store frames ", frame_directory, " created!")
	else:
		print("Folder to store frames already exists!")

	#Iterating through the files in the folder
	for filename in os.listdir("/tmp"):
		if filename.endswith(".mp4") or filename.endswith(".MP4"):
			print("FILES WE ARE ITERATING  ", filename)
			create_frames("/tmp/"+filename, frame_directory)
	

	#Send all the  frames for each video into the face_recognition API and get the result
	recognize_face(frame_directory)
	
	
	
def writeOutputToS3(path, data):
	header = ["name", "major", "year"]
	with open(path, 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(header)
		writer.writerow(data)
	session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=AWS_REGION
	)
	s3 = session.client("s3")
	for filename in os.listdir("/tmp"):
		if filename.endswith(".csv") or filename.endswith(".CSV"):
			print("Uploading to output bucket..  name: " + str(filename)) 
			s3.upload_file("/tmp/"+filename, output_bucket, filename)
			print("Upload to s3 complete")



def getVideosfromS3(bucket, video_name):
	
	session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=AWS_REGION
	)
	s3 = session.client("s3")
	key = video_name

	video_download_path = "/tmp"
	video_path = os.path.join(video_download_path, '{}'.format(key))
	response = s3.list_objects(Bucket = bucket)
	print("Listing objects in bucket ", response)
	s3.download_file(Bucket=bucket, Key=key, Filename=video_path)
	print("Printing the temp folder after downloading files from s3 bucket",os.listdir("/tmp"))


def create_frames(video_path, frames_dir):
	# Create the frames directory if it doesn't exist
	frame_name = video_path.split("/")[-1].split(".")[0]
	# Extract frames from the video using ffmpeg
	(
		ffmpeg
		.input(video_path)
		.filter("fps", fps=1)
		.output(frames_dir+"/"+frame_name+".jpg", format='image2', vframes=1)
		.run()
	)

def recognize_face(path):
		
	#Known face encodings data
	known_encoding_data = open_encoding("encoding")
	face_names = list(known_encoding_data['name'])
	known_face_encodings = list(known_encoding_data['encoding'])
	
	
	for filename in os.listdir(path):
		
		#Unknown face encodings (first frame of the video)
		unknown_image = face_recognition.load_image_file(path+"/"+filename)
		unknown_encodings = face_recognition.face_encodings(unknown_image)[0]
	
		results = face_recognition.compare_faces(known_face_encodings, unknown_encodings)
		names_with_result = list(zip(face_names, results))
		print(names_with_result, "FILE = ", filename)
	
		temp_name = str(filename).split(".")[0]
		for items in names_with_result:
			if items[1] == True:
				result = items[0]
				break
		print("OUTPUT OF THE FACE RECOGNITION IS : ", result)
		dynamodb_client = boto3.resource('dynamodb')
		table = dynamodb_client.Table('ndk-proj2-table')
		response = table.get_item(
			Key={
				'name' : result
			}
		)
		res_name = result
		res_major = response['Item']['major']
		res_year = response['Item']['year']
		print("Final queried output : ", res_name, res_major, res_year)
		writeOutputToS3("/tmp/"+temp_name+".csv", [res_name, res_major, res_year])
		

if __name__ == "__main__":
	#Ignore (for local testing purposes)
	with open('/Users/dnayani/Desktop/test.json') as f:
		event = json.load(f)
	face_recognition_handler(event, None)

