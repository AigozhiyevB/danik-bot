# Use an official Python runtime as a parent image
FROM public.ecr.aws/lambda/python:3.11
#FROM python:3.11-alpine

# Set the working directory in the container
WORKDIR /var/task

COPY danik_bot ./danik_bot
COPY data ./data
COPY docker/prod_reqs.txt ./


# Install any needed packages specified in prod_reqs.txt
RUN pip install --upgrade pip && \
    pip install -r prod_reqs.txt

# Command to run the application
CMD ["danik_bot.lambda_handler"]
