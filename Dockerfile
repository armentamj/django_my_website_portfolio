FROM python:3.12-slim

RUN mkdir /app
WORKDIR /app

# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 

# Install system dependencies (gettext for i18n)
RUN apt-get update && apt-get install -y \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything from local folder
COPY src/ ./

# Migrate Database
RUN python manage.py migrate

# Compile i18n translation files
# (This converts your .po files into .mo binary files)
RUN python manage.py compilemessages

# Collect all static files (Tailwind CSS, Local Fonts, Images) 
# so WhiteNoise can find them
RUN python manage.py collectstatic --noinput

# Start the server with Daphne (best for WebSockets)
# Expose the Django port
EXPOSE 8000
 
# Run Django’s development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
