import csv
import json
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from poi.models import PointOfInterest

class Command(BaseCommand):
    help = 'Import PoI data from CSV, JSON, and XML files'

    def add_arguments(self, parser):
        parser.add_argument('file_paths', nargs='+', type=str)

    def handle(self, *args, **options):
        for file_path in options['file_paths']:
            if file_path.endswith('.csv'):
                self.import_csv(file_path)
            elif file_path.endswith('.json'):
                self.import_json(file_path)
            elif file_path.endswith('.xml'):
                self.import_xml(file_path)
            else:
                self.stdout.write(self.style.ERROR(f'Unsupported file type: {file_path}'))

    def import_csv(self, file_path):
        with open(file_path, mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                try:
                    latitude = float(row['poi_latitude'])
                    longitude = float(row['poi_longitude'])
                    ratings = self.parse_ratings(row.get('poi_ratings', '[]'))
                    average_rating = sum(ratings) / len(ratings) if ratings else 0
                    self.create_or_update_poi({
                        'external_id': row['poi_id'],
                        'name': row['poi_name'],
                        'latitude': latitude,
                        'longitude': longitude,
                        'category': row['poi_category'],
                        'average_rating': average_rating
                    })
                except ValueError as e:
                    self.stdout.write(self.style.ERROR(f"Error processing row: {e}"))
                    continue  # Skip this row and continue with the next


    def import_json(self, file_path):
        with open(file_path, mode='r') as json_file:
            data = json.load(json_file)
            for item in data:
                average_rating = sum(item['ratings']) / len(item['ratings']) if item['ratings'] else 0
                self.create_or_update_poi({
                    'external_id': item['id'],
                    'name': item['name'],
                    'latitude': item['coordinates']['latitude'],
                    'longitude': item['coordinates']['longitude'],
                    'category': item['category'],
                    'average_rating': average_rating
                })

    def import_xml(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        for item in root.findall('DATA_RECORD'):
            ratings_str = item.find('pratings').text
            ratings = [int(r) for r in ratings_str.split(',')] if ratings_str else []
            average_rating = sum(ratings) / len(ratings) if ratings else 0
            self.create_or_update_poi({
                'external_id': item.find('pid').text,
                'name': item.find('pname').text,
                'latitude': float(item.find('platitude').text),
                'longitude': float(item.find('plongitude').text),
                'category': item.find('pcategory').text,
                'average_rating': average_rating
            })

    def create_or_update_poi(self, poi_data):
        poi, created = PointOfInterest.objects.update_or_create(
            external_id=poi_data['external_id'],
            defaults={
                'name': poi_data['name'],
                'latitude': poi_data['latitude'],
                'longitude': poi_data['longitude'],
                'category': poi_data['category'],
                'average_rating': poi_data['average_rating']
            }
        )
        action = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{action} PoI: {poi.name} with external ID {poi.external_id}"))

    def parse_ratings(self, ratings_str):
        # Strip curly braces and parse the string into a list of floats
        ratings_str = ratings_str.strip('{}')
        try:
            return [float(r) for r in ratings_str.split(',')]
        except ValueError:
            return []
