#!/bin/bash
git pull
# Ensure the folder exists and is writable
mkdir -p static_prod
chmod -R 777 static_prod 
docker compose up -d --build
