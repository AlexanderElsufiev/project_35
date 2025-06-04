# СОЗДАНО ПО ОПИСАНИЮ В УРОКЕ 28.2
import os
from celery import Celery

# указание где искать основные настройки
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mcdonalds.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# app = Celery('mcdonalds')
app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     # 'action_every_30_seconds': {
#     #     'task': 'tasks.action',
#     #     'schedule': 30,
#     #     'args': ("some_arg"),
#     # },
#
#     # 'print_every_5_seconds': {
#     #     'task': 'news.tasks.hello',
#     #     'schedule': 7,
#     #      'args': ('stroka',),
#     # },
#     'post_news_week_every_5_seconds': {
#         'task': 'news.tasks.send_news',
#         'schedule': 30,
#          'args': (),
#     },
#
# }

from celery.schedules import crontab

# ЧТОБЫ НЕ МЕШАЛО, УБИРАЮ РЕГУЛЯРНУЮ ОТПРАВКУ ПОЧТЫ!
app.conf.beat_schedule = {
    # 'post_news_week_every_monday_8': {
    #     'task': 'news.tasks.send_news',
    #     'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    #     'args': (),
    # },
    # 'post_news_every_10min': {
    #     'task': 'news.tasks.send_news',
    #     'schedule': crontab( minute='*/10'),
    #     # 'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    #     'args': (),
    # },

    # 'action_every_monday_8am': {
    #     'task': 'action',
    #     'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    #     'args': (agrs),
    # },
}



