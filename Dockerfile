FROM python:3.12-slim
WORKDIR /app

# Install system dependencies (gettext for i18n)
RUN apt-get update && apt-get install -y \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything from local folder
COPY .src/ ./

# Compile i18n translation files
# (This converts your .po files into .mo binary files)
RUN python manage.py compilemessages

# Collect all static files (Tailwind CSS, Local Fonts, Images) 
# so WhiteNoise can find them
RUN python manage.py collectstatic --noinput

# Start the server with Daphne (best for WebSockets)
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "config.asgi:application"]
