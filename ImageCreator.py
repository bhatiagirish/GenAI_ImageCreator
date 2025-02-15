#
# ImageCreator.py
# Version 1.0
# Created on Sat Mar 23 2024
# Created By Girish Bhatia
# Copyright (c) 2024
#


import boto3
import json
import logging
import os
import base64
import datetime


logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info("Loading function")

# create a bedrock runtime client
client_runtime = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

# create a s3 client
s3_client = boto3.client("s3")

# get values for environment variables
# throw exception if environment variables are not set

modelId = os.environ["modelId"]
logger.info(f"modelId is --> {modelId}")
if modelId is None:
    logger.info("modelId is None")
    raise Exception("modelId is not set")

# Lambda function to invoke bedrock founddation model
# will invoke titen LLM
def lambda_handler(event, context):
    prompt = ""
    if event is None:
        logger.info("Event is None")
        return buildResponse(400, "Event is not set")

    # extract txt file from the event based on post method
    if event.get("httpMethod") == "POST":
        logger.info("httpMethod is POST")
        prompt = event.get("body")
        contentType = event.get("headers").get("content-type")
    else:
        logger.info("httpMethod is not POST")
        return buildResponse(400, "Only POST method is supported")

    if prompt is None:
        logger.info("prompt is None")
        return buildResponse(
            400, "No prompt found. A prompt must be provided to process the request"
        )
    # create promptBody to generate an image
    promptBody = json.dumps(
        {
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {"text": prompt},
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "quality": "standard",
                "cfgScale": 8.0,
                "height": 512,
                "width": 512,
                "seed": 0,
            },
        }
    )

    response = client_runtime.invoke_model(body=promptBody, modelId=modelId)
    responseBody = json.loads(response["body"].read())
    base64_image_data = responseBody["images"][0]

    # decode base64 image data
    image_data = base64.b64decode(base64_image_data)

    # build image name with date and time stamp
    img_time = datetime.datetime.now()
    # img_time = datetime.datetime.strptime(str(img_time), '%Y-%m-%d %H:%M:%S.%f')
    img_time = img_time.strftime("%Y-%m-%d_%H-%M-%S_%f")
    logger.info(f"img_time is --> {img_time}")
    image_name = f"image_{img_time}.png"
    logger.info(f"image_name is --> {image_name}")

    # upload image to s3 bucket
    try:
        uploadImgToS3(image_data, "gbbedrock", image_name)
        logger.info("image uploaded to target bucket")
        return buildResponse(200, "Image uploaded to target bucket")
    except Exception as e:
        logger.error(f"Error uploading image to target bucket: {e}")
        return buildResponse(400, "Error uploading image to target bucket")


# function to build responde based on status code and message
def buildResponse(statusCode, message):
    return {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
        },
        #'body': json.dumps(message)
        "body": message,
    }


# function to upload JSON to s3 bucket
def uploadImgToS3(image_data, bucket_name, s3_file_name):
    try:
        s3_client.put_object(Body=image_data, Bucket=bucket_name, Key=s3_file_name)
        logger.info("image uploaded to target bucket")
        return True
    except Exception as e:
        logger.error(f"Error uploading image to target bucket: {e}")
        return None
