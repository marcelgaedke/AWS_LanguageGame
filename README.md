# AWS Language Game

A language learning game application built using AWS Serverless Application Model (SAM), combining frontend and backend components.

## Project Structure
```
.
├── frontend
│   ├── assets                      #game assets: images and audio files
│   │   ├── audio
│   │   │   ├── animals
│   │   │   ├── colors
│   │   │   ├── fruits
│   │   │   └── vegetables
│   │   └── images
│   │       ├── animals
│   │       ├── categories
│   │       ├── colors
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
│   ├── add-new-game-objects.py       #utility script for adding new objects to the game
└── template.yaml                     #sam template

```

## Prerequisites

- AWS CLI configured with appropriate credentials
- AWS SAM CLI installed
- Python 3.x
- Node.js and npm (for frontend)
- AWS Account with appropriate permissions

## Features

- DynamoDB-backed storage
- Audio generation using Amazon Polly
- Frontend application for user interaction
- Serverless backend infrastructure
- Language addition and management capabilities

## Setup and Deployment

1. **Install Dependencies**
   ```bash
   # Install backend dependencies
   sam build

   # Install frontend dependencies
   cd frontend
   npm install

2. **Configure Environment Variables**

Create a .env file based on the provided template

Configure necessary AWS credentials and settings

3. **Deploy the Application**

4. **Build and Deploy Frontend**

cd frontend
npm run build


## Local Development
1. **Run Backend Locally**

sam local start-api

2. **Run Frontend Locally**

cd frontend
npm start


## Utility Scripts
add-new-game-objects.py: Script for adding new objects to the game


## Project Components
**Frontend** : Web interface for user interaction

**Backend** : Serverless functions handling game logic

**Database** : DynamoDB for data persistence

**Audio** : Amazon Polly integration for language pronunciation

## Backup and Maintenance
DynamoDB backups are stored in the dynamodb-backup directory

Regular maintenance scripts are available in the scripts directory

## Security
Environment variables are used for sensitive configuration

AWS IAM roles and policies manage access control

Secure API endpoints for frontend-backend communication

## Contributing
Fork the repository

Create a feature branch

Commit your changes

Push to the branch

Create a Pull Request

License
Add your license information here