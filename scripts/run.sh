#!/bin/bash
echo "Start the application using uvicorn..."

uvicorn --app-dir /mnt/ src.main:app --host 0.0.0.0 --port 9090