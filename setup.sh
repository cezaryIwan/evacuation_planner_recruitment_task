#!/bin/bash

set -e

echo "=== Tworzenie projektu ==="
PROJECT_DIR="evac_routing_service"
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

echo "=== Tworzenie wirtualnego środowiska ==="
python -m venv venv
source venv/bin/activate

echo "=== Instalacja FastAPI i Uvicorn ==="
pip install --upgrade pip
pip install fastapi uvicorn

echo "=== Tworzenie struktury projektu ==="
mkdir -p app/api
mkdir -p app/core
mkdir -p app/services
mkdir -p app/models

cat << 'EOF' > app/main.py
from fastapi import FastAPI

app = FastAPI(title="Evacuation Routing Service")
EOF

echo "=== Tworzenie requirements.txt ==="
pip freeze > requirements.txt