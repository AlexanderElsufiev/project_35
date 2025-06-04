from django.core.management.base import BaseCommand, CommandError

#
# class Command(BaseCommand):
#     help = 'Подсказка вашей команды'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
#     missing_args_message = 'Недостаточно аргументов'
#     requires_migrations_checks = True  # напоминать ли о миграциях. Если true — то будет напоминание о том, что не сделаны все миграции (если такие есть)
#
#     def add_arguments(self, parser):
#         # Positional arguments
#         parser.add_argument('argument', nargs='+', type=int)
#
#     def handle(self, *args, **options):
#         # здесь можете писать любой код, который выполняется при вызове вашей команды
#         self.stdout.write(str(options['argument']))


from django.core.management.base import BaseCommand, CommandError
from news.models import Post


class Command(BaseCommand):
    help = 'Подсказка вашей команды - ДЕЛАЕТ РЕЙТИНГИ ВСЕХ ПОСТОВ = ВВЕДЁННОМУ ИСХОДНО АРГУМЕНТУ, ЕСЛИ ЭТО ЦЕЛОЕ ЧИСЛО'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True  # напоминать ли о миграциях. Если true — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('argument', nargs='+', type=int)

    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполнится при вызове вашей команды
        self.stdout.readable()
        self.stdout.write(
            'ХОТИТЕ СДЕЛАТЬ РЕЙТИНГИ ВСЕХ ПОСТОВ =5? yes/no')  # спрашиваем пользователя, действительно ли он хочет удалить все товары
        answer = input()  # считываем подтверждение

        if answer == 'yes':  # в случае подтверждения действительно удаляем все товары
            # Product.objects.all().delete()
            zn=options['argument']
            for post in Post.objects.all():
                post.raiting=zn[0]
                post.save()
            self.stdout.write(self.style.SUCCESS('Succesfully wiped products!'))
            return

        self.stdout.write(
            self.style.ERROR('Access denied'))  # в случае неправильного подтверждения, говорим, что в доступе отказано


