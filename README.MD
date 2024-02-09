# Clone the repository
git clone https://github.com/Emmywise/searchsmartly

# Navigate to the project directory
cd searchsmartly

# Set up a virtual environment
python -m venv venv
source venv/bin/activate  # Use `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create a superuser for the Django Admin Panel
python manage.py createsuperuser

# runserver
python manage.py runserver

# to run the application
# csv
python manage.py import_pois data/pois.csv

# for xml
python manage.py import_pois data/pois.xml

# for json
python manage.py import_pois data/pois.json

# to run the test
python manage.py test poi.tests.test_import_pois_command.ImportPoisCommandTestCase

# I added the files in the repository for easier testing
