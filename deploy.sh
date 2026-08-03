#!/bin/bash
echo "Pulling latest code from Git..."
git pull

#Completely wipe the server's static folders
echo "Cleaning old static files..."
rm -rf static_prod

# Ensure folders exist
echo "Creating the static_prod directory..."
mkdir -p static_prod
chmod -R 777 static_prod 

# Stopping the current containers to unlock file access
echo "Stopping container..."
docker compose down

# Rebuild and start
echo "Building and starting container..."
docker compose up -d --build --force-recreate

# WAIT for the container to be ready
echo "Waiting for container to start..."
sleep 5

# Run migrations
docker compose exec mdwp python manage.py migrate --noinput

# Collect static files if you changed CSS/JS
echo "Collecting static files..."
docker compose exec mdwp python manage.py collectstatic --noinput --clear

echo "Deployment finished!"
