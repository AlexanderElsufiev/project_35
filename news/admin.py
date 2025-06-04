from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Category, Post


def null_raiting(modeladmin, request, queryset): # все аргументы уже должны быть вам знакомы, самые нужные из них это request — объект хранящий информацию о запросе и queryset — грубо говоря набор объектов, которых мы выделили галочками.
    queryset.update(raiting=-5)
null_raiting.short_description = 'Обнулить рейтинги =-5' # описание для более понятного представления в админ панеле задаётся, как будто это объект


# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    # list_display = [field.name for field in Post._meta.get_fields()]  # генерируем список имён всех полей для более красивого отображения
    # ТАК СОЗДАННЫЙ СПИСОК НЕ РАБОТАЕТ!
    # list_display===['postcategory', 'post_comm', 'id', 'author', 'tip', 'time_in', 'zagolov', 'text', 'raiting', 'likes', 'dislikes', 'categorys', 'comments']
    # В НЁМ ЕСТЬ ЛИШНИЕ = # 'postcategory','post_comm',  'categorys', 'comments'
    # print(f'list_display==={list_display}')
    # list_display = ('zagolov','text','raiting','post_bon')
    list_display = ['id','author','post_bon','tip','time_in','zagolov','text','raiting','likes',]
    list_filter = ('raiting', 'author','tip') # добавляем примитивные фильтры в нашу админку
    search_fields = ('raiting','author') # тут всё очень похоже на фильтры из запросов в базу
    actions = [null_raiting] # добавляем действия в список

# Register your models here.
# ЭТО ПОЗВОЛЯЕТ ДОБИТЬСЯ НАЛИЧИЯ РАЗДЕЛА NEWS НА СТРАНИЦЕ АДМИНИСТРАТОРА,
# С КОНКРЕТНЫМИ ГРАФАМИ - Category, Post / ДО ЭТОГО ИХ НЕ БЫЛО
admin.site.register(Category)
# admin.site.register(Post)
admin.site.register(Post,PostAdmin)

# ИЗ РАЗДЕЛА NEWS УБИРАЕЕТСЯ Post
# admin.site.unregister(Post) # разрегистрируем
# ПОСЛЕ ИСЧЕЗНОАВЕНИЯ И КАТЕГОРИЙ - РАЗДЕЛ NEWS ПРОПАДАЕТ СОВСЕМ!
# admin.site.unregister(Category)