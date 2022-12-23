
# Running OpenAI Whisper on AWS lambda using AWS ECR Image




## Setup

#### Download the trained whisper model

```
  Downlad the whisper trained model from
  https://openaipublic.azureedge.net/main/whisper/models/ed3a0b6b1c0edf879ad9b11b1af5a0e6ab5db9205f891f668f8b0e6c6326e34e/base.pt
  and copy and rename it to local_base.pt in base folder
```

#### Whisper module
Git is not supported inside dockor. We will use another way to install whisper module inside container

```
  
  git submodule add https://github.com/openai/whisper.git  _submodules/whisper
```

#### Build dockor image
Now build the dockor image
```
  sudo docker build -t ecr_whisper .

```

#### Steps to deploy to ECR
##### 1) Go to Amazon Elastic Container Registry
##### 2) Create a private repository as lambda doesn't support public ones :
##### 3. Now use this command to log in and obtain privileges
```
  aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com

```
##### 4) Next use this command to add a tag to the image you have created
```
  docker tag <docker_image_id> ecr_uri

```
##### 5) Run this to push the image to the repository in AWS.

```
  docker push ecr_uri

```


#### Steps to deploy to AWS Lambda
Now that your image is in ECR, open the Lambda console

Select container image option in AWS lambda function page.
Put the image URI and create

Note: Select max memory to 10240 MB (depends on how much larger your mp3 files are)
#### Now Go to S3 bucket and set the trigger to Lambda

Finished. You can now test it by uploading mp3 file to S3 bucket and lmabda will create transription and srt file into S3 bucket.
