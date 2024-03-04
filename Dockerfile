# Use the official Python image as a parent image
FROM python:3.10
# The environment variable ensures that the python output is set straight
# to the terminal without buffering it first
ENV PYTHONUNBUFFERED 1


RUN mkdir /IntellasureBackend
WORKDIR /IntellasureBackend
ADD . /IntellasureBackend/

# Install any needed packages specified in requirements.txt
RUN pip freeze > requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000
EXPOSE 8000

# Define environment variable
ENV FLASK_APP = intellasure_flask_app.py
ENV DB_HOST = "iintellasurecluster-instance-1.cm7ngpomtctj.us-west-1.rds.amazonaws.com"
ENV DB_NAME = "IntellasureDB"
ENV DB_USER = "intellasure"
ENV DB_PASSWORD = "1SunnyDay!"


# Run gunicorn when the container launches
CMD gunicorn -b :8000 intellasure_flask_app:app