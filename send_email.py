import os, sys, datetime
import django
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ['DJANGO_SETTINGS_MODULE'] = 'Scraping_service.settings'

django.setup()
from scraping.models import Vacancy, Error, Url
from Scraping_service.settings import EMAIL_HOST_USER

User = get_user_model()
today = datetime.datetime.today()
subject = 'JF'
text_content = f'Рассылка вакансий за {today}'
from_email = EMAIL_HOST_USER
empty = '<h2>К сожалению на сегодня по вашим параметрам данных нет :(</h2>'


qs = User.objects.filter(send_email=True).values('city', 'language', 'email')

user_dict = {}
for i in qs:
    user_dict.setdefault((i['city'], i['language']), [])
    user_dict[(i['city'], i['language'])].append(i['email'])

if user_dict:
    params = {'city_id__in': [], 'language_id__in': []}
    for pair in user_dict.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])
    qs = Vacancy.objects.filter(**params, timestamp=today).values()

    vacancies = {}
    # for i in qs:
    #     vacancies.setdefault((i['city_id'], i['language_id']), [])
    #     vacancies[(i['city_id'], i['language_id'])].append(i)
    #
    # for keys, emails in user_dict.items():
    #     rows = vacancies.get(keys, [])
    #     html = ''
    #     for row in rows:
    #         html += f'<h5><a href="{row["url"]}">{row["title"]}</a></h5>'
    #         html += f'<p>{row["description"]}</p>'
    #         html += f'<p>{row["company"]}</p><br><hr>'
    #     _html = html if html else empty
    #
    #     for email in emails:
    #         to = email
    #         msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    #         msg.attach_alternative(_html, "text/html")
    #         msg.send()

qs = Error.objects.filter(timestamp=today)
subject = ''
text_content = ''
to = EMAIL_HOST_USER
content = ''

if qs.exists():
    error = qs.first()
    data = error.data
    for i in data:
        content = f'<h5><a href="{i["url"]}">Error: {i["title"]}</a></h5>'

    subject = f'Ошибки скрапинга за {today}'
    text_content = f'Ошибки скрапинга за {today}'


qs = Url.objects.all().values('city', 'language')
urls_dict = {(i['city'], i['language']): True for i in qs}
urls_err = ''
for keys in user_dict.keys():
    if keys not in urls_dict:
        urls_err += f'<p>Для города: {keys[0]} и  ЯП: {keys[1]} отсутствуют URL</p>'

if urls_err:
    subject += ' Отсутствующие Url'
    content += urls_err

if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(content, "text/html")
    msg.send()