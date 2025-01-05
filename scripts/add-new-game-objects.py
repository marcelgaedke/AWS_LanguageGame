#Script for adding new objects to the game by iterating over the new image files
#english word of the image must be at the beginning of the filename of the image
#iterate of the image files
#upload each image to s3
#extract english word from image filename
#generate translations for other languages
#generate audio files for the words using polly
#upload audio files to s3
#add all metadata into dynamodb

#Usage: 
# modify the IMAGE_DIR and CATEGORY variables to match your requirements
# set Environment Variables S3_BUCKET_NAME and DYNAMODB_TABLE_NAME
# python3 add-new-game-objects.py
#


#Change these according to requirements
IMAGE_DIR = '/srv/temp/images'      #local directory where image files are stored
CATEGORY = 'colors'                 #game category for the images


import boto3
import os
from botocore.exceptions import BotoCoreError, NoCredentialsError
import re


# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
polly = boto3.client('polly')
translate = boto3.client('translate')
s3 = boto3.client('s3')

# Get environment variables
DYNAMODB_TABLE_NAME = os.environ.get('DYNAMODB_TABLE_NAME')  # Set Environment Variable DYNAMODB_TABLE_NAME
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')            # Set Environment Variable S3_BUCKET_NAME

# Define constants
AUDIO_PREFIX = 'audio'                       # Prefix for audio files in the S3 bucket
IMAGE_PREFIX = 'images'                       # Prefix for images in the S3 bucket

LANGUAGES_DICT = {
    'italian': { 
        'voice_id': 'Bianca', 
        'language_code': 'it-IT',
        'target_language_code': 'it'
    }, 
    'german': {
        'voice_id': 'Vicki',
        'language_code': 'de-DE',
        'target_language_code': 'de'
    }, 
    'english': {
        'voice_id': 'Joanna',
        'language_code': 'en-US',
        'target_language_code': 'en'
    },
    'spanish': {
        'voice_id': 'Lucia',
        'language_code': 'es-ES',
        'target_language_code': 'es'
    },
    'french': {
        'voice_id': 'Lea',
        'language_code': 'fr-FR',
        'target_language_code': 'fr'
    }
}



#function to upload audio content to s3 !does not work for files
def upload_to_s3(bucket_name, key, content):
    """
    Upload content to an S3 bucket.
    :param bucket_name: The name of the S3 bucket
    :param key: The key (path) for the file
    :param content: The file content
    """
    print(f"Uploading audio to s3://{bucket_name}/{key}")
    try:
        s3.put_object(Bucket=bucket_name, Key=key, Body=content)
        print(f"Uploaded audio to s3://{bucket_name}/{key}")
    except BotoCoreError as e:
        print(f"Error uploading file to S3: {e}")
       
        
#function to generate audio from text
def generate_audio(text, language_code, voice_id):
    """
    Generate audio from text using Amazon Polly.
    :param text: The text to convert to speech
    :param language_code: The language code for the voice
    :param voice_id: The ID of the voice to use
    :return: The audio content as bytes
    """
    try:
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            Engine='generative',
            LanguageCode=language_code,
            VoiceId=voice_id
        )
        return response['AudioStream'].read()
    except BotoCoreError as e:
        print(f"Error generating audio for word '{text}': {e}")
        return None

#function to translate english word to other languages using aws translate
def translate_text(text, target_language_code):
    """
    Translate text using Amazon Translate.
    :param text: The text to translate
    :param target_language_code: The target language code
    :return: The translated text
    """
    try:
        response = translate.translate_text(
            Text=text,
            SourceLanguageCode='en',
            TargetLanguageCode=target_language_code
        )
        return response['TranslatedText']
    except BotoCoreError as e:
        print(f"Error translating text '{text}': {e}")
        return None


#function to add item to dynamodb with attributes: category,"english","english_audio_url","german","german_audio_url","image_url","italian","italian_audio_url" 
def add_item_to_dynamodb(table_name, category, english_word, image_url, english_audio_url, german_word, german_audio_url, italian_word, italian_audio_url, spanish_word, spanish_audio_url, french_word, french_audio_url):
    """
    Add an item to the DynamoDB table.
    :param category: The category of the item
    :param english_word: The English word
    :param image_url: The URL of the image
    :param english_audio_url: The URL of the English audio
    :param german_word: The German word
    :param german_audio_url: The URL of the German audio
    :param italian_word: The Italian word
    :param italian_audio_url: The URL of the Italian audio
    """
    table = dynamodb.Table(table_name)
    try:
        table.put_item(
            Item={
                'category': category,
                'english': english_word,
                'image_url': image_url,
                'english_audio_url': english_audio_url,
                'german': german_word,
                'german_audio_url': german_audio_url,
                'italian': italian_word,
                'italian_audio_url': italian_audio_url,
                'spanish': spanish_word,
                'spanish_audio_url': spanish_audio_url,
                'french': french_word,
                'french_audio_url': french_audio_url
            }
        )
        print(f"Added item to DynamoDB: {english_word}")
    except BotoCoreError as e:
        print(f"Error adding item to DynamoDB: {e}")


if __name__ == "__main__":
    #iterate over all files in /srv/temp/images and display filename
    for filename in os.listdir(IMAGE_DIR):
        #get file extension
        file_basename = os.path.splitext(filename)[0]
        file_extension = os.path.splitext(filename)[1]
        #get english word from filename
        english_word = file_basename.replace('-', ' ').replace('-', ' ').lower()
        print(f"english_word: {english_word}")
        print(f"{filename} - {english_word}")
        

        #upload image file to s3
        image_bucket_key = f"{IMAGE_PREFIX}/{CATEGORY}/{english_word}{file_extension}"
        if file_extension == '.jpg':
            content_type='image/jpeg'
        elif file_extension == '.png':
            content_type='image/png'
            
        #upload file to s3 from path
        try:
            s3.upload_file(f"{IMAGE_DIR}/{filename}", S3_BUCKET_NAME, image_bucket_key, ExtraArgs={'ContentType': content_type})
            print(f"Uploaded image {IMAGE_DIR}/{filename} to s3://{S3_BUCKET_NAME}/{image_bucket_key}")
            
        except BotoCoreError as e:
            print(f"Error uploading file to S3: {e}")
        
        
        #upload_file_to_s3(bucket_name=S3_BUCKET_NAME, key=bucket_key, file_path=f"{IMAGE_DIR}/{filename}")
               
        #initialize empty dictionary for translated words
        translated_words = {}
        
        #initialize empty dictionary for audio urls
        audio_urls = {}
        
        #generate audio files for german and italian words and upload to s3
        for language, language_dict in LANGUAGES_DICT.items():
            if language == 'english':
                translated_word = english_word
            else:
                translated_word = translate_text(english_word, language_dict['target_language_code'])
                print(f"translated english: {english_word} into {language}: {translated_word} ")
                #add translated word to dictionary
                translated_words[language] = translated_word
            print(f"Generating audio for {language} word: {translated_word} with {language_dict['language_code']} {language_dict['voice_id']}")
            audio_content = generate_audio(translated_word, language_dict['language_code'], language_dict['voice_id'])
            if audio_content:
                # Construct the S3 key for the audio file
                audio_bucket_key = f"{AUDIO_PREFIX}/{CATEGORY}/{english_word.replace(' ', '_')}_{language}.mp3"

                # Upload the audio file to S3
                upload_to_s3(S3_BUCKET_NAME, audio_bucket_key, audio_content)
                
                #add audio url to dictionary
                audio_urls[language] = f"{english_word.replace(' ', '_')}_{language}.mp3"
            else:
                print(f"Failed to generate audio for word: {english_word}")
            
        print(f"audio_urls: {audio_urls}")
        #add item to dynamodb
        image_url = f"{english_word}{file_extension}"
        print(f"adding item {english_word} to dynamodb")
#       #add_item_to_dynamodb(table_name=DYNAMODB_TABLE_NAME, category=CATEGORY, english_word=english_word, image_url=image_url, english_audio_url=audio_urls['english'] , german_word=translated_words['german'], german_audio_url=audio_urls['german'], italian_word=translated_words['italian'], italian_audio_url=audio_urls['italian'])

        table = dynamodb.Table(DYNAMODB_TABLE_NAME)
        try:
            table.put_item(
                Item={
                    'category': CATEGORY,
                    'english': english_word,
                    'image_url': image_url,
                    'english_audio_url': audio_urls['english'],
                    'german': translated_words['german'],
                    'german_audio_url': audio_urls['german'],
                    'italian': translated_words['italian'],
                    'italian_audio_url': audio_urls['italian'],
                    'spanish': translated_words['spanish'],
                    'spanish_audio_url': audio_urls['spanish'],
                    'french': translated_words['french'],
                    'french_audio_url': audio_urls['french']
                }
            )
            print(f"Added item to DynamoDB: {english_word}")
        except BotoCoreError as e:
            print(f"Error adding item to DynamoDB: {e}")
            
        