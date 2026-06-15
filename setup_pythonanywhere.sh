#!/bin/bash
# PythonAnywhere Bash console'da ishga tushiring: bash setup_pythonanywhere.sh

echo "=== Virtual environment yaratish ==="
python3.13 -m venv .venv
source .venv/bin/activate

echo "=== Paketlarni o'rnatish ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== .env faylni yarating (qo'lda to'ldiring) ==="
cp .env.example .env
echo ">>> .env faylini nano yoki vi bilan to'ldiring: nano .env"

echo "=== Migration ==="
python manage.py makemigrations accounts
python manage.py migrate

echo "=== Static fayllar ==="
python manage.py collectstatic --noinput

echo "=== Superuser yarating ==="
python manage.py createsuperuser

echo "=== Tayyor! ==="
