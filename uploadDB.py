import json
import boto3
from boto3.dynamodb.conditions import Key
import csv

with open("student_data.json") as student_data:
    student_table = json.load(student_data)

dynamodb = boto3.resource('dynamodb')
dbtable = dynamodb.Table('ndk-proj2-table')
for i in range(0, len(student_table)):
    dbtable.put_item(Item=student_table[i])

# dynamodb_client = boto3.resource('dynamodb')
# table = dynamodb_client.Table('ndk-proj2-table')
# response = table.get_item(
#     Key={
#         'name' : 'president_trump'
#     }
# )
# print(response['Item']['year'])
# name = "Carlos"
# age = 10
# year = 2000

# # Define the header row for the CSV file
# header = ['name', 'age', 'year']

# # Define the row data for the CSV file
# data = [name, age, year]

# # Create a CSV file and write the header and row data to it
# with open('/Users/dnayani/Documents/ASU/Misc/output.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(header)
#     writer.writerow(data)