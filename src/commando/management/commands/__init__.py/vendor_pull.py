from django.core.management.base import BaseCommand
from typing import Any
from django.conf import settings
import helpers


STATICFILES_VENDOR_DIR = getattr(settings,'STATICFILES_VENDOR_DIR')

VENDOR_STATICFILES ={
    "flowbite.im.css" : "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.css",
    "flowbite.im.js" : "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js",
}
class Command(BaseCommand):
    

    def handle(self, *args: Any, **options: Any):
        self.stdout.write("Downloading Vendor static files")
        completed_urls = []
        for  name,url in VENDOR_STATICFILES.items():
        
            out_path = STATICFILES_VENDOR_DIR / name
            dl_success = helpers.download_to_local(url,out_path)
            if dl_success:
                completed_urls.append(url)
            else:
             self.stdout.writer(
                self.style.ERROR(f'Failed to download {url}')
             )
            

        if set(completed_urls) == set(VENDOR_STATICFILES.values()):
            self.stdout.writer(
                self.style.SUCCESS('Successfully updated vendor static files')
            )
        else:
             self.stdout.writer(
                self.style.WARNING('Some files were not updated')
             )