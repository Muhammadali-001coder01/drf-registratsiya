python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install django djangorestframework
pip freeze > requirements.txt
# loyiha va app
django-admin startproject config .
python manage.py startapp library
