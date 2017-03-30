# Command to take migration names, return the SQL
# basically something to print out what migrations would be made
# when you run migrate (migrate.sh = "python manage.py migrate") 
# because you made changes to your model

# You can also check for problems with "python manage.py check"
# without making migrations or touching the database
python manage.py sqlmigrate polls 0001
