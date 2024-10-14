#!/bin/bash

API_NAME=$(basename "$PWD")
SERVICE_DIR="/etc/systemd/system"
CURRENT_DIR="$PWD"
GUNICORN_WORKERS=3
GUNICORN_BIND="0.0.0.0:8000"

# Создаем .service файл
cat << EOF > "${API_NAME}.service"
[Unit]
Description=${API_NAME} Flask API
After=network.target

[Service]
User=root
WorkingDirectory=${CURRENT_DIR}
Environment="PATH=${CURRENT_DIR}/.venv/bin"
ExecStartPre=/usr/bin/git config --global --add safe.directory ${CURRENT_DIR}
ExecStartPre=/usr/bin/git pull origin main
ExecStart=${CURRENT_DIR}/.venv/bin/gunicorn --workers ${GUNICORN_WORKERS} --bind ${GUNICORN_BIND} main:app
Restart=always
RestartSec=10
StandardOutput=append:${CURRENT_DIR}/api.log
StandardError=append:${CURRENT_DIR}/api.log

[Install]
WantedBy=multi-user.target
EOF

# Копируем .service файл в системную директорию
sudo cp "${API_NAME}.service" "${SERVICE_DIR}/"

# Перезагружаем конфигурацию systemd
sudo systemctl daemon-reload

# Включаем сервис
sudo systemctl enable "${API_NAME}.service"

# Запускаем сервис
sudo systemctl start "${API_NAME}.service"

echo "Сервис ${API_NAME} создан и запущен"