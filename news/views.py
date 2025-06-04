from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView

from .models import Post, Author
from .filters import PostFilter
from .forms import PostForm

# ДЛЯ РАСПРЕДЕЛЕНИЯ ПРАВ ПОЛЬЗОВАТЕЛЕЙ
from django.contrib.auth.mixins import PermissionRequiredMixin

from datetime import datetime
from datetime import date


# ДЛЯ ПОДПИСКИ ПОЛЬЗОВАТЕЛЯ
from .models import Subscribers #Subscription
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SubscriptionForm
from .models import Subscribers

# ДЛЯ КЭША
from django.core.cache import cache # импортируем наш кэш

@login_required
def subscribe_view(request): # ПРОЦЕДУРА РАБОТАЕТ В МОМЕНТ ОФОРМЛЕНИЯ ПОДПИСОК, В http://127.0.0.1:8000/subscribe/
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            categories = form.cleaned_data['categories']
            # Удаляем существующие подписки пользователя
            Subscribers.objects.filter(user=request.user).delete()
            # Создаем новые подписки
            for category in categories:
                Subscribers.objects.create(user=request.user, category=category)
            # return redirect('subscription_success')  # Перенаправление после успешной подписки
            return redirect('/')  # Перенаправление после успешной подписки  было redirect('news/')
    else:
        # form = SubscriptionForm() #так мы брали пустые категории, даже если уже были
        # Получаем текущие категории, на которые подписан пользователь
        user_categories = Subscribers.objects.filter(user=request.user).values_list('category', flat=True)
        form = SubscriptionForm(initial={'categories': user_categories})
    return render(request, 'protect/index_subscribe.html', {'form': form})


# ВСЁ ОСТАЛЬНОЕ


class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    # model = Product - меняем - показывать будем посты!
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-time_in'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'post_list.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    # context_object_name = 'products' - меняем на Посты - пока не знаю где их описать - ЭТО АДРЕС ССЫЛКИ
    context_object_name = 'posts'
    paginate_by = 8  # вот так мы можем указать количество записей на странице

class ArtList(PostsList):
    paginate_by = 6
    # показываем только статьи
    def get_queryset(self):
        return Post.objects.filter(tip='t').order_by('-time_in')



class PostsListSearch(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'post_list_search.html'
    context_object_name = 'posts'
    paginate_by = 7  # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset().order_by('-time_in')
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали в этом юните ранее.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset

        # Удаляем параметр page из строки запроса - чтобы при пагинации работали переходы
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            query_params.pop('page')
        context['filter_query'] = query_params.urlencode()
        return context

class ArtListSearch(PostsListSearch):  # наследуется всё что можно из первого варианта
    def get_queryset(self):
        queryset = super().get_queryset().filter(tip='t').order_by('-time_in')
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


# ДОБАВЛЯЕМ НОВЫЙ КЛАСС
#  Он отличается от ListView тем, что возвращает конкретный объект,  а не список всех объектов из БД
class PostDetail(PermissionRequiredMixin, DetailView):
    permission_required = ('news.view_post',)  # название права на добавление постов
    # form_class = PostForm # ЭТО ДОБАВКА ДЛЯОТОБРАЖЕНИЯ КАТЕГОРИЙ
    model = Post    # Указываем нашу разработанную форму
    template_name = 'post_uno.html' # Используемый шаблон — product.html
    context_object_name = 'post' # Название объекта, в котором будет выбранный пользователем продукт
    # ДАЛЕЕ ДЛЯ КЭШИРОВАНИЯ:
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'post-{self.kwargs["pk"]}',None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.
        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)
        return obj
    # КОНЕЦ НУЖНОГО ДЛЯ КЕШИРОВАНИЯ

class ArtDetail (PostDetail):
    pass


# Добавляем новое представление для создания товаров.
class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)  # название права на добавление постов
    # fields = ['title', 'content'] # не нужна, потому что есть строка form_class = PostForm
    # Указываем нашу разработанную форму
    form_class = PostForm
    model = Post  # модель товаров
    # и новый шаблон, в котором используется форма.
    # template_name = 'post_edit.html' # заменил на специальный с фиксированным автором
    template_name = 'post_create.html'
    success_url = reverse_lazy('post_list')  # путь после успешного ввода
    # ПРИНУДИТЕЛЬНО СТАВИМ ПАРАМЕТР НОВОСТЬ
    param = 'n'  # Атрибут класса
    def form_valid(self, form):
        # ТО ЧТО БЫЛО РАНЬШЕ - ПОСТАНОВКА ВСЕХ ПАРАМЕТРОВ ПОСТА
        form.instance.tip = self.param  # Новость - из параметра
        user = self.request.user # Получаем текущего пользователя
        author, created = Author.objects.get_or_create(user=user) # Получаем или создаем объект Author, связанный с текущим пользователем
        form.instance.author = author  # Устанавливаем автора поста

        return super().form_valid(form)




class ArtCreate(PostCreate):
    param = 't'  # будем писать как кстатью
    success_url = reverse_lazy('art_list')

# Добавляем представление для изменения товара.
class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)  # название права на добавление постов
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    # путь после успешного ввода
    success_url = reverse_lazy('post_list')

class ArtUpdate(PostUpdate):
    success_url = reverse_lazy('art_list')


# Представление удаляющее товар.
class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)  # название права на добавление постов
    model = Post
    template_name = 'post_delete.html'
    # путь после успешного ввода
    success_url = reverse_lazy('post_list')


class ArtDelete(PostDelete):
    pass

# представление запускающеесяс главной страницы сайта, урок 4/7   28.4. Создание простых задач
from django.http import HttpResponse
from django.views import View
from .tasks import hello, printer
from datetime import datetime, timedelta

class IndexViewTask(View):
    def get(self, request):
        hello.apply_async('HELLO=',countdown=5)
        printer.delay(10)
        return HttpResponse('Hello!')




# УРОК 3/7   35.3 Перевод текстовой информации в шаблонах КУРС Локализации ЦЕЛЬ перевод на другой язык
from django.utils.translation import gettext as _  # импортируем функцию для перевода


# пробник на перевод
class Index(View):
    def get(self, request):
        string = _('Hello world and my_str')
        return HttpResponse(string)


# пробник на перевод
class Index2(View):
    def get(self, request):
        string = _('Hello world and MY_ds')
        context={'string':string}
        return HttpResponse(render(request,'index.html',context))





