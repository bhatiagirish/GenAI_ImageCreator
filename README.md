# Image Creator Lambda Function

## Overview
This Lambda function uses Amazon Bedrock's image generation capabilities to create images from text prompts and store them in an S3 bucket. 
The function accepts text prompts via HTTP POST requests and returns the status of the image generation and upload process.

## Features
- Text-to-image generation using Amazon Bedrock
- Automatic image storage in S3
- Unique image naming with timestamps
- HTTP POST endpoint support
- CORS-enabled responses

- ## Prerequisites
- AWS Lambda environment
- Required IAM permissions for:
  - Amazon Bedrock
  - Amazon S3
  - CloudWatch Logs
- Environment Variables:
  - `modelId`: The Amazon Bedrock model ID to use for image generation

## Configuration
The function requires the following environment variable:
- `modelId`: The identifier for the Bedrock foundation model to use

## Input Format
The function expects HTTP POST requests with the following:
- Method: POST
- Body: Text prompt for image generation
- Content-Type: application/json

## Image Generation Parameters
Default image generation configuration:
- Number of images: 1
- Quality: standard
- CFG Scale: 8.0
- Image dimensions: 512x512 pixels
- Seed: 0

## Output
The function returns a JSON response with:
- Status code (200 for success, 400 for errors)
- CORS headers
- Response message indicating success or failure

## Error Handling
The function includes error handling for:
- Missing or invalid prompts
- Unsupported HTTP methods
- S3 upload failures
- Missing environment variables

## Function Flow
1. Validates HTTP method and prompt
2. Generates image using Bedrock
3. Converts base64 response to image data
4. Creates unique filename with timestamp
5. Uploads to S3 bucket
6. Returns success/failure response

## S3 Storage
Images are stored in the specified S3 bucket with the naming format:
`image_YYYY-MM-DD_HH-MM-SS_microseconds.png`

## Dependencies
- boto3
- json
- logging
- os
- base64
- datetime

