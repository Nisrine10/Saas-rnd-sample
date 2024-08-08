from django.core.management.base import BaseCommand
from typing import Any
import helpers


VENDOR_STATICFILES ={
    "flowbite.im.css" : "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.css",
    "flowbite.im.js" : "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js",
}
class Command(BaseCommand):
    

    def handle(self, *args: Any, **options: Any):
        self.stdout.write("Downloading Vendor static files")

        for  name,url in VENDOR_STATICFILES.items():
            print(name,url)