import json
import os, sys


project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ['DJANGO_SETTINGS_MODULE'] = 'Scraping_service.settings'


import django
django.setup()

from django.db import DatabaseError
from scraping.parser.parsers import *
from scraping.models import Vacancy, City, Language, Error


parsers = (
    (get_work_ua, 'https://www.work.ua/jobs-kyiv-python/'),
    (get_dou_ua, 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D1%97%D0%B2&category=Python'),
    (djinni_co, 'https://djinni.co/jobs/?location=kyiv&region=UKR&primary_keyword=Python')
)

city = City.objects.filter(slug='kiev').first()
language = Language.objects.filter(slug='python').first()
jobs, errors = [], []

for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:
    v = Vacancy(**job, city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    er = Error(data=errors).save()

# with open('jobs.txt', 'a', encoding='utf-8') as file:
#     json.dump(jobs, file, indent=4, ensure_ascii=False)
