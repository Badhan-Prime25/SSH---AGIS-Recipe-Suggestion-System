FROM python:3.13-slim

WORKDIR /app

# Install system dependencies including X11 libraries, Qt, and Xvfb for GUI applications
RUN apt-get update && apt-get install -y --no-install-recommends \
    libxkbcommon0 libgl1 libegl1-mesa libglib2.0-0 libdbus-1-3 \
    libxcb-xinerama0 libxcb-cursor0 libfontconfig1 libfreetype6 libx11-xcb1 \
    libxcomposite1 libxi6 libxrandr2 libxcursor1 libxtst6 libxrender1 \
    libxfixes3 libxdamage1 libxshmfence1 libxcb1 libxcb-util1 \
    fonts-dejavu-core xvfb xauth \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Qt and X server on Windows
ENV QT_QPA_PLATFORM_PLUGIN_PATH=/usr/lib/qt/plugins/platforms
ENV DISPLAY=host.docker.internal:0
# Use host.docker.internal to connect to the Windows X server

# Copy the application code into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the application with Xvfb
CMD ["xvfb-run", "-a", "python", "Recipe_GUI.py"]
