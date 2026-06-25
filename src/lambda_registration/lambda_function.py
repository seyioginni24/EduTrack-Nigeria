import json
import boto3
import os


dynamodb = boto3.resource('dynamodb')
sqs = boto3.client('sqs')

TABLE_NAME = 'EduTrack-Transcripts'
QUEUE_URL = 'https://sqs.af-south-1.amazonaws.com/435392105553/EduTrack-Registration-Queue'

def lambda_handler(event, context):
    try:
     
       
        body = json.loads(event['body'])
        
        university_id = body.get('University_ID')
        student_id = body.get('Student_ID')
        first_name = body.get('First_Name')
        last_name = body.get('Last_Name')
        department_id = body.get('Department_ID')
        
        if not university_id or not student_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing tenant identifier (University_ID) or Student_ID'})
            }
            
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(
            Item={
                'University_ID': university_id,  # Strict partition boundary
                'Student_ID': student_id,        # Sort key identifier
                'First_Name': first_name,
                'Last_Name': last_name,
                'Department_ID': department_id
            }
        )
        
        message_body = {
            'University_ID': university_id,
            'Student_ID': student_id,
            'First_Name': first_name,
            'Last_Name': last_name
        }
        
        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(message_body)
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Student {student_id} successfully registered under {university_id}.'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }