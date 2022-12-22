# Pull the base image with python 3.8 as a runtime for your Lambda
FROM public.ecr.aws/lambda/python:3.8

# Copy the earlier created requirements.txt file to the container
COPY requirements.txt ./

# Install the python requirements from requirements.txt
# Install submodule packages
COPY whisper _submodules/whisper

RUN pip install _submodules/whisper

# copy whisper model to the container
COPY local_base.pt ./

# copy ffmpeg mmodule to the container
COPY ffmpeg ./
RUN chmod -R 777 /var/task/ffmpeg

# Copy the created app.py file to the container
COPY app.py ./

# Set the CMD to your handler
CMD ["app.lambda_handler"]