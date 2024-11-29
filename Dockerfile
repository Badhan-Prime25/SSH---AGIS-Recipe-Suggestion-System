# Base Image
FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for GUI applications
RUN apt-get update && apt-get install -y --no-install-recommends \
    libxkbcommon0 libgl1 libegl1-mesa libglib2.0-0 libdbus-1-3 \
    libxcb-xinerama0 libxcb-cursor0 libfontconfig1 libfreetype6 libx11-xcb1 \
    libxcomposite1 libxi6 libxrandr2 libxcursor1 libxtst6 libxrender1 \
    libxfixes3 libxdamage1 libxshmfence1 libxcb1 libxcb-util1 \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the DISPLAY environment variable (for X11 forwarding)
ENV DISPLAY=host.docker.internal:0.0

# Run the application
CMD ["python", "Recipe_GUI.py"]
