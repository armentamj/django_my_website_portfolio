#!/bin/bash
git pull

# Ensure folders exist
mkdir -p static_prod
chmod -R 777 static_prod 

# Rebuild and start
docker compose up -d --build

# WAIT for the container to be ready
echo "Waiting for container to start..."
sleep 5

# Run migrations
docker compose exec mdwp python manage.py migrate --noinput
# Optional: Collect static files if you changed CSS/JS
docker compose exec web python manage.py collectstatic --noinput

echo "Deployment finished!"
