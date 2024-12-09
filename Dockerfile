#  Image
FROM python:3.13-slim

# Setting the working directory
WORKDIR /app

# Copying the code into the container
COPY . /app

# Installing all the  Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Running the  Recipe logic test
CMD ["python", "RSS_Logic_Test.py"]
