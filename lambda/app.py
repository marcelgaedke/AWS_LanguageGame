import boto3
import json
import os
import random

print('Loading function')
dynamo_client = boto3.client('dynamodb', region_name='eu-central-1')


def lambda_handler(event, context):
    
    #Parse Variables from event
    #print("Received event: " + json.dumps(event, indent=2))   #for debugging
    table_name = os.environ.get('AWS_DYNAMODB_TABLE_NAME')
    print("Table Name: " + table_name)
    print("Method: " + event['requestContext']['http']['method'])
    #print event query string parameters
    category = event['queryStringParameters']['category']
    language = event['queryStringParameters']['language']
    print(f"language: {language}, category: {category}")
    #print resource path
    ressource_path = event['requestContext']['http']['path']
    print("Resource Path: " + ressource_path)
    

    if event['requestContext']['http']['method'] == 'GET':
        print("Method GET")
            
        #try to query dynamoDB for items in requested category
        try:      

            table_query = dynamo_client.query(
                TableName=table_name,
                KeyConditionExpression='category = :category',
                ExpressionAttributeValues={
                    ':category': {'S': category}
                }
            )
            
            #select random correct and incorrect items
            random_display_items = random.sample(table_query['Items'], 4)
            correct_item = random_display_items[0]
            incorrect_items = [x['image_url']['S'] for x in random_display_items[1:]]
        
            #return json response
            language_audio_url = f"{language}_audio_url"
            body ={
                    "category": category,
                    "word": correct_item[language]['S'],
                    "audioUrl": correct_item[language_audio_url]['S'],
                    "correctImage": correct_item['image_url']['S'],
                    "incorrectImages": incorrect_items
                }
            statusCode = '200'
        
        except Exception as e:
            body = {"Error": str(e)}
            statusCode = '400'
            print(f"An unexpected error occurred: {str(e)}")
      
        return {
            'statusCode': statusCode,
            'headers': {
                'Content-Type': 'application/json',
            },
            'body': json.dumps(body),
            "isBase64Encoded": False
        }
        
        