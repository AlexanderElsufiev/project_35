from celery import shared_task
import time

@shared_task
def hello(str):
    print("Hello, world!")
    print(f"str={str}")
    time.sleep(5)
    print("Hello, world после 5 сек!")



@shared_task
def printer(N):
    print('PRINTER_BEG')
    for i in range(N):
        time.sleep(1)
        print(i+1)
    print('PRINTER_END')


@shared_task
def post_mail(*args,**kwargs):
    # print(f"FORM ={str(form)}")
    # author=form.instance.author
    print(f"POST_PRINT=")





# ОТПРАВКА ПОЧТЫ В МОМЕНТ ВОЗНИКНОВЕНИЯ
import datetime

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import PostCategory, Post
from django.template.loader import render_to_string


# ПРОГРАММА ОТСЫЛКИ ПИСЕМ В МОМЕНТ НАПИСАНИЯ ПОСТА, ВЗЯТА ИЗ signals, И СМЕНЕНО НАЗВАНИЕ И
@shared_task
def send_notifications2(preview,pk,title,subscribers): #программа собственно отсылки писем
    html_content= render_to_string (
        'post_created_email.html', #ФАЙЛ собственно текста письма - он создаётся в templates/
        {'text':preview,'link':f"{settings.SITE_URL}/news/{pk}"} #красивая ссылка в почте на открытие собственно статьи
    )
    msg = EmailMultiAlternatives(
        subject = title,
        body = '',
        from_email = settings.DEFAULT_FROM_EMAIL, #от кого отправляютсявсе письма по умолчанию
        to = subscribers,
    )
    msg.attach_alternative(html_content,'text/html') # сформированный выше шаблон с указанием формата
    msg.send() # собственно отсылка



# ПРОГРАММА ОТСЫЛКИ ПИСЕМРАЗ В НЕДЕЛЮ, ВЗЯТА ИЗ NEWS/management/commands/runapscheduler.py (my_job)
# СМЕНЕНО НАЗВАНИЕ НА БЛАГОЗВУЧНОЕ

from news.models import PostCategory, Post
import datetime
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

@shared_task
def send_news():
    kol_day=7 #ЗА СКОЛЬКО ДНЕЙ БЕРЁМ СПИСОК НОВОСТЕЙ
    print(f"hello from job =NEWS= {datetime.now()}")
    print('Post='+str(Post))
    # today = datetime.date.today()
    today = datetime.now().date()
    to_day= today - timedelta(days=kol_day)
    posts = Post.objects.filter(time_in__date__gte=to_day)
    spisok = {} # БУДУЩИЙ СПИСОК ОТСЫЛОК

    for pst in posts:
        emails = []
        cats=pst.categorys.all()
        for cat in cats:
            subscribers = cat.subscribers.all()
            emails += [s.user.email for s in subscribers if s.user.email]
        emails = list(set(emails))  # ДЕЛАЮ СПИСОК УНИКАЛЬНЫХ ПОЧТ
        content=f"<h2>Появилась новая <a href= {settings.SITE_URL}/news/{pst.pk}> статья </a>"
        content += f" в разделе куда вы подписаны. </h2> <p>Заголовок='{pst.zagolov}'</p> <p>Превью='{pst.preview()}'</p> "
        # print(f"КРАСИВАЯ ОТСЫЛКА = {content}")
        for email in emails:
            if not email in spisok:spisok[email]=[]
            spisok[email].append(content)
    # print(f"spisok={spisok}")
    # ТЕПЕРЬ СОБСТВЕННО ОТСЫЛКА ПИСЕМ
    for email in spisok:
        posti=spisok[email]
        lettre='<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>УВЕДОМЛЕНИЕ!</title></head><body>'
        lettre+=f"<p>За последние {kol_day} дней в чате появились следующие новости:</p>"
        for pst in posti:
            lettre+=pst
        lettre += f"</body></html>"
        msg = EmailMultiAlternatives(
            subject='Уведомление по почте',
            body=f"В приложении список статей за последние {kol_day} дней, которые вы могли случайн оне увидеть на сайте",
            from_email=settings.DEFAULT_FROM_EMAIL,  # от кого отправляютсявсе письма по умолчанию
            to=[email],
        )
        msg.attach_alternative(lettre, 'text/html')  # сформированный выше шаблон с указанием формата
        msg.send()  # собственно отсылка




