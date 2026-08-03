#!/bin/bash
git pull

# Stop the current containers to unlock file access
docker compose down

#Completely wipe the server's static folders
rm -rf static_prod

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
# Collect static files if you changed CSS/JS
docker compose exec mdwp python manage.py collectstatic --noinput --clear

echo "Deployment finished!"
