#!/bin/bash

#Synchronize local frontend with remote s3 Bucket
#Usage:
#S3BUCKETNAME="<bucketname>" ./scripts/deploy_frontend.sh

aws s3 sync frontend/assets/ s3://${S3BUCKETNAME}	#synchronize static assets with s3 bucket
aws s3 sync frontend/src/prod/ s3://${S3BUCKETNAME}     #synchronize frontend code html,css,js with remote bucket
