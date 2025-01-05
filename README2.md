# Language Game on AWS

This repository contains the code and infrastructure for the **Language Game**, a cloud-native application built on AWS. The game aims to help users learn new languages interactively. It leverages AWS services such as Lambda, DynamoDB, S3, and CloudFront to provide a serverless architecture.

## Project Structure

```
.
├── frontend
│   ├── assets                      # game assets: images and audio files
│   │   ├── audio
│   │   │   ├── animals
│   │   │   ├── colors
│   │   │   ├── fruits
│   │   │   └── vegetables
│   │   └── images
│   │       ├── animals
│   │       ├── categories
│   │       ├── colors
│   │       ├── flags
│   │       ├── fruits
│   │       └── vegetables
│   └── src                          # static frontend code: HTML, JS, and CSS files
│       ├── dev                      
│       └── prod
├── lambda
│   ├── app.py                       # Lambda function for game setup
│   └── requirements.txt
├── README.md
├── scripts
│   ├── add-new-game-objects.py      # Utility script for adding new objects to the game
└── template.yaml                    # SAM template
```

## Features

- **Frontend:**
  - Hosted on S3 and distributed via CloudFront.
  - Static files (HTML, CSS, JavaScript) for game pages and user interactions.
  - Assets include categorized images and audio files for the game.

- **Backend:**
  - AWS Lambda function (`app.py`) for serverless business logic.
  - DynamoDB table (`language-game`) with primary key `category` and sort key `english`.

- **Infrastructure:**
  - Defined using AWS SAM for easy deployment and management.
  - Secure communication between the frontend and backend.

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

## Getting Started

### Prerequisites

- Install the [AWS CLI](https://aws.amazon.com/cli/) and configure it with proper credentials.
- Install the [AWS SAM CLI](https://aws.amazon.com/serverless/sam/).
- Python 3.8+ (for backend development).

### Deployment

#### 1. Deploy the Backend and Infrastructure
```bash
sam build
sam deploy --guided
```
Follow the prompts to configure the stack name, region, and S3 bucket for deployment artifacts.

#### 2. Deploy the Frontend
Navigate to the `frontend/src/prod` directory and upload the files to the S3 bucket:
```bash
aws s3 sync prod/ s3://<your-s3-bucket-name> --acl public-read
```

#### 3. Invalidate CloudFront Cache (Optional)
Run the script to invalidate cached assets:
```bash
aws cloudfront create-invalidation --distribution-id <distribution-id> --paths "/*"
```

### Local Development

#### Running the Backend Locally
Use SAM to start a local API Gateway and Lambda runtime:
```bash
sam local start-api
```

#### Testing
Run unit tests for the backend:
```bash
cd lambda
pytest
```

## Contributions

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- Built with AWS SAM and other AWS services.
- Inspired by serverless design patterns for scalable applications.

---
Feel free to reach out with any questions or suggestions!

