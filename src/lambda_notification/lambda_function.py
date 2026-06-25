import json
import boto3

sns = boto3.client('sns')

SNS_TOPIC_ARN = 'arn:aws:sns:af-south-1:435392105553:EduTrack-Registration-Notification'

def lambda_handler(event, context):
    for record in event['Records']:
        
        payload = json.loads(record['body'])
        
        university_id = payload.get('University_ID')
        student_id = payload.get('Student_ID')
        first_name = payload.get('First_Name')
        last_name = payload.get('Last_Name')
        
        subject = f"EduTrack Alert: New Registration at {university_id}"
        message = f"Hello Admin,\n\nA new student has been registered to your institution.\n\nUniversity: {university_id}\nStudent ID: {student_id}\nName: {first_name} {last_name}\n\nSystem: EduTrack Nigeria"
        
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=subject,
            Message=message
        )
        
    return {
        'statusCode': 200,
        'body': 'Notifications processed successfully'
    }