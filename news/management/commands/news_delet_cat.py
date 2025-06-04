
from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Подсказка вашей команды'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        cat=options["category"]
        answer = input(f'Вы правда хотите удалить все статьи в категории {cat}? yes/no:')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR(f'Отменено, вы ввели ={answer}'))
            return
        try:
            categ = Category.objects.get(category=cat)
            # categ = Category.objects.get(id=1)
            self.stdout.write(self.style.SUCCESS(f'НАЙДЕНА КАТЕГОРИЯ {categ} = {categ.category}'))

            kol=0
            Post.objects.filter(postcategory__category=categ).delete()

            # for post in Post.objects.filter(postcategory__category=categ):
            #     post.raiting=-1
            #     post.save()
            #     kol+=1
            # self.stdout.write(self.style.SUCCESS(f'ЯКОБЫ УДАЛИЛ ИЗ КАТЕГОРИИ {categ} ПОСТОВ {kol} ШТУК')) # в случае неправильного подтверждения говорим, что в доступе отказано

        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'НЕТ КАТЕГОРИИ {cat}'))

# сперва пришлось создать категорию с латинским именем klass1
# python manage.py news_delet_cat klass1
# python manage.py news_delet_cat СТИХИ: - НЕ РАБОТАЕТ