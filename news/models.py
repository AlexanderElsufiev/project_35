

from django.db import models
from datetime import datetime
from django.db.models import Sum
from django.core.cache import cache

from django.contrib.auth.models import User
# class User(models.Model):
#     fio = models.CharField(max_length=100, default='')
#     time_in = models.DateTimeField(auto_now_add=True)
#     interes = models.CharField(max_length=100,default='')
#     # raiting = models.IntegerField(default=0)
#     # likes = models.IntegerField(default=0)
#     # dislikes = models.IntegerField(default=0)


class Author(models.Model):
   # user = models.ForeignKey(User, on_delete=models.CASCADE)
   # сделаем максимум 1 автора на 1 пользователя
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   raiting = models.IntegerField(default=0)
   kolzap = models.IntegerField(default=0)
   timezap = models.DateTimeField(auto_now_add=True)

   def __str__(self):
       return self.user.username

   def update_rating(self):
       # 1. Суммарный рейтинг всех постов автора, умноженный на 3
       raiting_post = self.author_post.aggregate(total=models.Sum('raiting'))['total'] or 0
       raiting_comm = self.user.user_comm.aggregate(total=models.Sum('raiting'))['total'] or 0
       raiting_post_comm = Comment.objects.filter(post__author=self).aggregate(total=models.Sum('raiting'))[
                                      'total'] or 0
       # raiting_post_comm = self.author_post.all().post_comm.(total=models.Sum('raiting'))['total'] or 0
       self.raiting = raiting_post*3+raiting_comm+raiting_post_comm
       self.save()


class Category(models.Model):
    category = models.CharField(max_length=50, default='', unique=True)

    # Обратите внимание, что мы дополнительно указали методы __str__ у моделей.
    # Django будет их использовать, когда потребуется где-то напечатать наш объект целиком
    def __str__(self):
        return self.category.title()



# класс подписок пользователей на категории
class Subscribers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subscribers')
    class Meta:
        unique_together = ('user', 'category')





# СПИСОК ЗАПРЕЩЁННЫХ СЛОВ
class Zapret(models.Model):
    zapret = models.CharField(max_length=50, default='', unique=True)
    # Для читаемости
    def __str__(self):
        return self.zapret.title()

# процедура удаления из текста запрещённых слов - перенесена в templatetags/custom_filters.py


class Post(models.Model):
    # pass
    txt = 't'
    news = 'n'
    TIPS = [(txt, 'Статья'),(news, 'Новость'),]
    # Дополнительное поле указатель на номера категорий
    categorys = models.ManyToManyField(Category, through = 'PostCategory')
    # авторы
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author_post')
    # ТИП стаитья или новость
    tip = models.CharField(max_length=1,choices=TIPS,default=txt)
    time_in = models.DateTimeField(auto_now_add=True)
    zagolov = models.CharField(max_length=100, default='')
    text = models.TextField()
    raiting = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    # Дополнительное поле указатель на комментарии
    comments = models.ManyToManyField(User, through = 'Comment')

    def like(self):
        self.likes += 1;self.raiting += 1
        self.save()
    def dislike(self):
        self.dislikes += 1;self.raiting -= 1
        self.save()

    def preview(self):
        stext = self.text[:123] + '...' if len(self.text) > 123 else self.text
        return stext

    # ДОБАВЛЯЮ СВОЙСТВО А НЕ РЕАЛЬНОЕ ПОЛЕ
    @property
    def post_bon(self):
        return self.raiting > 5

    # Обратите внимание, что мы дополнительно указали методы __str__ у моделей. Django будет их использовать, когда потребуется где-то напечатать наш объект целиком
    def __str__(self):
        # return f'{self.zagolov.title()}: {self.text[:20]} </br>'
        return f'{self.zagolov.title()}: {self.preview()} </br>'

    # ДЛЯ ХОРОШЕГО КЕШИРОВАНИЯ!
    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его
    # КОНЕЦ ДОБАВКИ ДЛЯ КЕШИРОВАНИЯ

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    class Meta:
        unique_together = ('post', 'category')


class Comment(models.Model):
    # pass
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name='post_comm')
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='user_comm')
    comment = models.CharField(max_length=255, default='')
    time_in = models.DateTimeField(auto_now_add=True)
    raiting = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def like(self):
        self.likes += 1;self.raiting += 1
        self.save()
    def dislike(self):
        self.dislikes += 1;self.raiting -= 1
        self.save()






