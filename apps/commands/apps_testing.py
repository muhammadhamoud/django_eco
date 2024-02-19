import django
import os
os.chdir(fr"C:\Backup\ng\backend")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import pandas as pd
import os
from django.conf import settings
df = pd.ExcelFile(os.path.join(settings.BASE_DIR, "fixtures", "roinsight.xlsx"))
site = df.parse(sheet_name='site')
for row in site.itertuples():
    site_info = SiteInformation(
        name=row.name,
        description=row.description,
        company_name=row.company_name,
        keywords=row.keywords,  # Generate a space-separated list of words
        )
    site_info.save()




# from django.utils.text import slugify
# name="Python is great.hamoud.test"
# filename = "test.test.txt"
# slug = slugify(name)
# name, ext = filename.split('.')
# new_filename = f"{slug}.{ext}"
# name, ext = os.path.splitext(filename)