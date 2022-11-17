#!/bin/bash

python3 -m pip install virtualenv
python3 -m venv venv

source venv/bin/activate

pip3 install -r requirements.txt

cd tfc

python3 manage.py migrate

echo "\n"
echo "Creating a new Admin User: \n"
echo "Suggested Username and Password: \n Username: admin \n Password: admin123 \n Email: admin@admin.com\n"
python3 manage.py createsuperuser
