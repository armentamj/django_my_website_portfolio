FROM python:3.12-slim

RUN mkdir /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# 1. Install system dependencies & Tailwind CLI
# 1. Install system dependencies & Tailwind CLI
RUN apt-get update && apt-get install -y \
    gettext \
    curl \
    && curl -sLO https://github.com \
    && chmod +x tailwindcss-linux-x64 \
    && mv tailwindcss-linux-x64 /usr/local/bin/tailwindcss \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Python dependencies
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy your source code (MUST happen before you try to build CSS)
COPY src/ ./

# 4. Build Tailwind CSS
# This uses the files you just copied in Step 3
RUN tailwindcss -i theme/static_src/src/styles.css -o theme/static/css/dist/styles.css --minify

# 5. Compile i18n
RUN python manage.py compilemessages

# 6. Collect Static
RUN python manage.py collectstatic --noinput

# 7. Migrate (Note: Keeping this here as requested, but ensure DB is accessible)
RUN python manage.py migrate

EXPOSE 8000
 
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
