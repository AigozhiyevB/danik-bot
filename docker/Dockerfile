# Use an official Python runtime as a parent image
FROM public.ecr.aws/lambda/python:3.11
#FROM python:3.11-alpine

# Set the working directory in the container
WORKDIR /app

COPY danik_bot /app/danik_bot
COPY data /app/data
COPY docker/prod_reqs.txt /app

# RUN apk add build-base

# Install any needed packages specified in prod_reqs.txt
RUN pip install --upgrade pip && \
    pip install -r prod_reqs.txt

# Command to run the application
CMD ["danik_bot.main.lambda_handler"]
