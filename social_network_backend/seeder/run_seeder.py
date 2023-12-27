import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_network_backend.settings")

import django
django.setup()

seeders = [
  'user_seeder'
]

for seeder_path in seeders:
  module = __import__(seeder_path)
  module.run()
