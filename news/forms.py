from django import forms
from django.core.exceptions import ValidationError
from .models import Post,  Category, Subscribers
from datetime import date



# ФОРМА ПОДПИСКИ НА КАТЕГОРИИ НОВОСТЕЙ
class SubscriptionForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Выберите категории для подписки"
    )
    class Meta:
        model = Subscribers
        fields = ['categories']  # Убедитесь, что это поле включено
        widgets = {'categories': forms.CheckboxSelectMultiple(),} # другой способ отображения. галочками




# ЭТО УЖЕ НЕ МОДЕЛЬ КАК Product, а некая форма, чуть иное описание
class PostForm(forms.ModelForm):
    # этот блок нужен для нормального отображения с помощью выбора многих ваариантов
    categorys = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # или SelectMultiple, если хочешь выпадающий список
        required=True,
        label='категория новостей (можно много вариантов, но минимум один)'
    )

    # description = forms.CharField(min_length=20)
    class Meta:
       # То, с чем форма обязана сравнить вводимые значения
       model = Post
       # можно взять вообще все поля (кроме id!) а можно перечислить только нужные
       fields = [ 'zagolov', 'text', 'raiting','categorys'] #убрать автора, чтобы не могли менять!
       # ЧТОБЫ АВТОР ПОКАЗЫВАЛСЯ НО НЕ ИЗМЕНЯЛСЯ - НЕ РАБОТАЕТ!!!
       # fields = ['author', 'zagolov', 'text', 'raiting']
       # widgets = {'author': forms.TextInput(attrs={'disabled': 'disabled'}),}

       labels = {
           'author': 'Автор',
           'zagolov': 'Заголовок',
           'text': 'Текст',
           'raiting': 'Рейтинг+',
           'categorys': 'категория новостей+'
       }

    def clean(self):
       cleaned_data = super().clean()

       text = cleaned_data.get("text")
       zagolov = cleaned_data.get("zagolov")
       if zagolov == text:
           raise ValidationError("Описание не должно быть идентичным названию.")

        # if text is not None and len(text) < 20:
        #     # ТЕКСТ ОШИБКИ = "{'text': ['Описание не может быть менее 20 символов.']}"
        #     raise ValidationError({"text": "Описание не может быть менее 20 символов."})

        # ЕЩЁ ДОБАВИЛЯЮ ПРОВЕРКУ НЕ БОЛЕЕ 6 СООБЩЕНИЙ В СУТКИ (ПЛЮС К 3 В 10 МИНУТ) - ПО ВИДЕО https://disk.yandex.ru/i/swu7JudE2Squ2Q
       author = cleaned_data.get('author') # НЕ РАБОТАЕТ - АВТОР НЕ ПЕРЕЧИСЛЕН В ПЕРЕЧНЕ fields = [ 'zagolov', 'text', 'raiting','categorys']
       today=date.today()
       kolpost=Post.objects.filter(author=author, time_in__date=today).count()
       print('KOLPOST='+str(kolpost)+ ' author='+str(author)+' today='+str(today))
       if kolpost>=6:
           raise ValidationError("ОГРАНИЧЕНИЕ 6 ПОСТОВ В СУТКИ (ПОМИМО 3 В 10 МИНУТ!) (FORMS.PY) ")

       return cleaned_data


    # def clean_name(self):
    #     name = self.cleaned_data["name"]
    #     if name[0].islower():
    #         raise ValidationError(
    #             "Название должно начинаться с заглавной буквы."
    #         )
    #     return name