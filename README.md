# AWS Language Game

This Game has been created for and submitted to the **AWS Game Builder Challenge** (https://devpost.com/software/aws-serverless-ai-powered-language-game)

This repository contains the code and infrastructure for a Children Language Game, a cloud-native application designed to help young children who cannot yet read or write learn new languages in an interactive and engaging way. The game uses a combination of images and AI-generated audio content to enhance the learning experience. Built on AWS, it leverages services such as Lambda, DynamoDB, S3, and CloudFront to deliver a serverless, scalable, and highly available architecture.


## Project Structure
```
.
├── frontend
│   ├── assets                      #game assets: images and audio files
│   │   ├── audio                   #audio files for each game category
│   │   │   ├── animals
│   │   │   ├── colors
│   │   │   ├── fruits
│   │   │   └── vegetables
│   │   └── images                  #image files for each game category
│   │       ├── animals
│   │       ├── categories
│   │       ├── colors
│   │       ├── favicon
│   │       ├── flags
│   │       ├── fruits
│   │       └── vegetables
│   └── src                           #static frontent code html, js and css files
│       ├── dev                       
│       └── prod
├── lambda
│   ├── app.py                        #lambda function for game setup
│   └── requirements.txt
├── README.md
├── scripts
|   ├── deploy_frontend.sh            #script to deploy frontend
│   ├── add-new-game-objects.py       #utility script for adding new objects to the game
└── template.yaml                     #sam template

```

## Prerequisites

- AWS CLI (https://aws.amazon.com/cli/) configured with appropriate credentials
- AWS SAM CLI (https://aws.amazon.com/serverless/sam/) installed
- Python 3.8+ (for backend development).
- AWS Account with appropriate permissions

## Features

- **Frontend:**
  - Hosted on S3 and distributed via CloudFront.
  - Static files (HTML, CSS, JavaScript) for game pages and user interactions.
  - Assets include categorized images and audio files for the game.

- **Backend:**
  - DynamoDB table (`language-game`) with primary key `category` and sort key `english`.
  - AWS Lambda function (`app.py`) for serverless business logic.
  - Serverless API Gateway with Lambda Integration

- **Infrastructure:**
  - Defined using AWS SAM for easy deployment and management.
  - Secure communication between the frontend and backend.

- **Scripts:**
  - deploy_frontend.sh - to automatically deploy frontend
  - add-new-game-objects.py - python script leveraging boto3 for adding new game object and creating new game categories

## Setup and Deployment

### Setup

#### 1. Deploy the Backend and Infrastructure
```bash
sam build
sam deploy --guided
```
Follow the prompts to configure the stack name, region, and S3 bucket for deployment artifacts.

#### 2. Deploy the Frontend
Get the bucket name from the output from the previous command and deploy the frontend using the script
```bash
S3BUCKETNAME="<bucketname>" ./scripts/deploy_frontend.sh
```

#### 3. Invalidate CloudFront Cache (Optional)
Run the script to invalidate cached assets:
```bash
aws cloudfront create-invalidation --distribution-id <distribution-id> --paths "/*"

```

## Local Development
1. **Create Test Event**
```bash
vi events/event.json 
{
  "key1": "value1",
  "key2": "value2",
  "key3": "value3"
}
```

2. **Test Lambda Function Locally**
```bash
sam local invoke --event events/event.json LanguageGameLambda
```


## Utility Scripts

#### Add new categories to the game
1. place image files in local directory 
2. ensure filenames correspond to english word of image content
3. modify the IMAGE_DIR and CATEGORY variables in the script to match your requirements
4. set Environment Variables S3_BUCKET_NAME and DYNAMODB_TABLE_NAME in terminal environment
5. run script
```bash
 python3 add-new-game-objects.py
```
6. the script will automatically translate the english words (filenames) into foreign languages,
generate audio files using **Amazon Polly**, upload the images and audio files to the s3 bucket,
store the image and audio urls as well as the translations into the dynamodb table

#### Frontend Deployment
1. run frontend deploy script after changes have been made
```bash
S3BUCKETNAME="<bucketname>" ./scripts/deploy_frontend.sh
```

## AWS Services Used

1. **Amazon S3**: Stores and serves static assets (frontend).
2. **Amazon CloudFront**: Distributes frontend content globally with low latency.
3. **AWS Lambda**: Executes backend logic.
4. **Amazon DynamoDB**: Stores game data.
5. **Amazon API Gateway**: Connects the frontend to backend Lambda functions.
6. **Amazon Translate**: Translates english words into foreign languges
7. **Amazon Polly**: AI Voice Generator to generate audio files from text
8. **AWS Serverless Application Model**: Deploy AWS Infrastructure as code
9. **Amazon Q**: AI Assistant for AWS Setup and Code Suggestions
10. **AWS SDK for Python (Boto3)**: Programmatic Interaction with AWS Ressources

## Security
* Environment variables are used for sensitive configuration
* AWS IAM roles and policies manage access control
* Secure API endpoints for frontend-backend communication

## Acknowledgments

- Built with AWS SAM and other AWS services as part of the AWS Game Builders Challenge (https://devpost.com/software/aws-serverless-ai-powered-language-game).
- Inspired by serverless design patterns for scalable applications.

---
Feel free to reach out with any questions or suggestions!