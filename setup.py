from distutils.core import setup

setup(
  name = 'coordinates-extractor',
  packages = ['coordinates_extractor'],
  package_dir = {'coordinates_extractor': 'coordinates_extractor'},
  package_data = {'coordinates_extractor': ['__init__.py', 'test/__init__.py', 'tests/test.py']},
  version = '0.4',
  description = 'Extract Coordinates from semi-structured text, like Wikipedia xml',
  author = 'Daniel J. Dufour',
  author_email = 'daniel.j.dufour@gmail.com',
  url = 'https://github.com/DanielJDufour/coordinates-extractor',
  download_url = 'https://github.com/DanielJDufour/coordinates-extractor/tarball/download',
  keywords = ['coordinates','extract','geo','gis','python','wiki','wikipedia'],
  classifiers = [],
)
