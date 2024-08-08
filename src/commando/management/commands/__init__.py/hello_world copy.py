from django.core.management.base import BaseCommand
from typing import Any

class Command(BaseCommand):
    help = 'Displays Hello World message'

    def handle(self, *args: Any, **options: Any):
        print("Hello, world!")
