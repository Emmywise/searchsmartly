from django.core.management import call_command
from django.test import TestCase
from unittest.mock import patch, MagicMock, mock_open
from poi.models import PointOfInterest

class ImportPoisCommandTestCase(TestCase):

    @patch('poi.models.PointOfInterest.objects.update_or_create')
    def test_import_csv(self, mock_update_or_create):
        # Set up the mock for PointOfInterest objects to simulate the database operation
        mock_poi_instance = MagicMock(spec=PointOfInterest)
        mock_update_or_create.return_value = (mock_poi_instance, True)

        # Valid CSV data
        mock_csv_data = "poi_id,poi_name,poi_category,poi_latitude,poi_longitude,poi_ratings\n"\
                        "1,Test POI,Category,10.123,-20.123,{3.0,4.0,3.0,5.0,2.0,3.0}"
        with patch('builtins.open', mock_open(read_data=mock_csv_data)):
            call_command('import_pois', 'dummy/path/test_pois.csv')

            ratings_list = [3.0, 4.0, 3.0, 5.0, 2.0, 3.0]
            average_rating = round(sum(ratings_list) / len(ratings_list), 0) 

            mock_update_or_create.assert_called_once_with(
                external_id='1',
                defaults={
                    'name': 'Test POI',
                    'category': 'Category',
                    'latitude': 10.123,
                    'longitude': -20.123,
                    'average_rating': average_rating 
                }
            )

    @patch('poi.models.PointOfInterest.objects.update_or_create')
    @patch('builtins.open', new_callable=mock_open, read_data='[{"id": "2", "name": "Test POI JSON", "coordinates": {"latitude": 20.123, "longitude": -30.123}, "category": "Category JSON", "ratings": [2, 3, 4]}]')
    def test_import_json(self, mock_file_open, mock_update_or_create):
        mock_poi_instance = MagicMock(spec=PointOfInterest)
        mock_update_or_create.return_value = (mock_poi_instance, True)

        call_command('import_pois', 'dummy/path/test_pois.json')

        ratings_list = [2, 3, 4]
        average_rating = sum(ratings_list) / len(ratings_list)

        mock_update_or_create.assert_called_once_with(
            external_id='2',
            defaults={
                'name': 'Test POI JSON',
                'latitude': 20.123,
                'longitude': -30.123,
                'category': 'Category JSON',
                'average_rating': average_rating
            }
        )

    @patch('poi.models.PointOfInterest.objects.update_or_create')
    @patch('xml.etree.ElementTree.parse')
    def test_import_xml(self, mock_parse, mock_update_or_create):
        mock_poi_instance = MagicMock(spec=PointOfInterest)
        mock_update_or_create.return_value = (mock_poi_instance, True)

        mock_root = MagicMock()
        mock_poi_element = MagicMock()
        mock_poi_element.find.side_effect = lambda tag: MagicMock(text={
            'pid': '3',
            'pname': 'Test POI XML',
            'platitude': '30.123',
            'plongitude': '-40.123',
            'pcategory': 'Category XML',
            'pratings': '2,3,4'
        }[tag])
        mock_root.findall.return_value = [mock_poi_element]
        mock_parse.return_value.getroot.return_value = mock_root

        call_command('import_pois', 'dummy/path/test_pois.xml')

        ratings_list = [2, 3, 4]
        average_rating = sum(ratings_list) / len(ratings_list)

        mock_update_or_create.assert_called_once_with(
            external_id='3',
            defaults={
                'name': 'Test POI XML',
                'latitude': 30.123,
                'longitude': -40.123,
                'category': 'Category XML',
                'average_rating': average_rating
            }
        )

