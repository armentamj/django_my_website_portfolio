FROM python:3.12-slim

RUN mkdir /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# 1. Install system dependencies & Tailwind CLI
RUN apt-get update && apt-get install -y gettext wget && wget -O /usr/local/bin/tailwindcss https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64 && chmod +x /usr/local/bin/tailwindcss && rm -rf /var/lib/apt/lists/*


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

EXPOSE 8000
 
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
