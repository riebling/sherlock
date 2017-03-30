# This command needs to be run to create database tables (from migrations)
# in other words, to apply the migrations created previously with makemigrations
# according to INSTALLED_APPS settings in settings.py
# Note there is no app name required, it gets them from <appname>/migrations
python manage.py migrate
