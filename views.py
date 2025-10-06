'''
Базовая структура ВСЕХ views:

def my_view(request):  # request - ВСЕГДА первый параметр
    # 1. Получить данные (из БД, форм, сессии)
    # 2. Обработать логику
    # 3. Подготовить данные для шаблона
    # 4. Вернуть HttpResponse
    return HttpResponse("Hello World")

Function-Based Views (FBV): 

1. Простой показ данных:

from django.shortcuts import render
from .models import MyModel  # Импортируем модель из текущего приложения

def show_data(request):
    """
    ФУНКЦИЯ ПРЕДСТАВЛЕНИЯ (VIEW) для отображения данных из базы данных
    
    Параметры:
    request - объект HttpRequest, содержащий информацию о запросе от пользователя
    (метод GET/POST, заголовки, параметры, данные формы и т.д.)
    """
    
    # ПОЛУЧЕНИЕ ДАННЫХ ИЗ БАЗЫ ДАННЫХ
    # MyModel.objects - менеджер объектов модели, обеспечивающий доступ к БД
    # .all() - метод, который выполняет SQL-запрос SELECT * FROM myapp_mymodel
    # Возвращает QuerySet - набор всех объектов модели MyModel
    data = MyModel.objects.all()
    
    # СОЗДАНИЕ КОНТЕКСТА ДЛЯ ШАБЛОНА
    # context - словарь, который передает данные из view в шаблон
    # Ключи словаря становятся переменными в шаблоне
    context = {
        'data': data  # Теперь в шаблоне будет доступна переменная {{ data }}
    }
    
    # ВОЗВРАТ HTML-СТРАНИЦЫ ПОЛЬЗОВАТЕЛЮ
    # Функция render() выполняет три действия:
    # 1. Загружает HTML-шаблон 'template.html'
    # 2. Заменяет переменные в шаблоне данными из context
    # 3. Возвращает готовый HttpResponse с HTML-кодом
    return render(request, 'template.html', context)

2. Детальная страница:
    
from django.shortcuts import render, get_object_or_404
from .models import MyModel  # Импортируем модель из текущего приложения

def detail_view(request, item_id):
    """
    ФУНКЦИЯ ПРЕДСТАВЛЕНИЯ ДЛЯ ПРОСМОТРА ОДНОГО КОНКРЕТНОГО ОБЪЕКТА
    
    Параметры:
    request - объект HttpRequest с информацией о запросе
    item_id - ID объекта, который нужно показать (из URL-адреса)
    """
    
    # ПОЛУЧЕНИЕ КОНКРЕТНОГО ОБЪЕКТА ИЗ БАЗЫ ДАННЫХ
    # get_object_or_404() - удобная функция Django, которая:
    # 1. Пытается найти объект по указанным критериям
    # 2. Если объект НАЙДЕН - возвращает его
    # 3. Если объект НЕ НАЙДЕН - автоматически возвращает страницу 404 (Not Found)
    #
    # Аргументы:
    # MyModel - модель, в которой ищем
    # id=item_id - критерий поиска: поле id должно равняться item_id
    # SQL-аналог: SELECT * FROM myapp_mymodel WHERE id = item_id;
    item = get_object_or_404(MyModel, id=item_id)
    
    # СОЗДАНИЕ КОНТЕКСТА ДЛЯ ШАБЛОНА
    # Передаем найденный объект в шаблон под именем 'item'
    context = {
        'item': item  # Теперь в шаблоне будет доступна переменная {{ item }}
    }
    
    # РЕНДЕРИНГ ШАБЛОНА С ДАННЫМИ
    # Загружает шаблон 'detail.html' и подставляет в него данные объекта
    return render(request, 'detail.html', context)


3. Форма с обработкой:

from django.shortcuts import render, redirect
from .forms import MyForm  # Импортируем нашу форму

def form_view(request):
    """
    ФУНКЦИЯ ДЛЯ ОБРАБОТКИ ФОРМ - СОЗДАНИЕ ИЛИ СОХРАНЕНИЕ ДАННЫХ
    
    Обрабатывает два типа запросов:
    - GET: Показывает пустую форму для ввода данных
    - POST: Обрабатывает отправленные данные формы
    """
    
    # ОБРАБОТКА POST-ЗАПРОСА (отправка формы)
    if request.method == 'POST':
        """
        Когда пользователь нажимает "Отправить" в форме,
        браузер отправляет POST-запрос с данными формы
        """
        
        # СОЗДАЕМ ФОРМУ С ДАННЫМИ ИЗ ЗАПРОСА
        # request.POST - словарь с данными, отправленными из формы
        form = MyForm(request.POST)
        
        # ПРОВЕРКА ВАЛИДНОСТИ ДАННЫХ
        if form.is_valid():
            """
            form.is_valid() проверяет:
            - Все ли обязательные поля заполнены
            - Корректны ли типы данных (email, числа, даты и т.д.)
            - Проходят ли кастомные валидаторы
            """
            
            # СОХРАНЕНИЕ ДАННЫХ В БАЗУ ДАННЫХ
            # form.save() создает новый объект модели и сохраняет в БД
            # SQL-аналог: INSERT INTO table_name (...) VALUES (...)
            form.save()
            
            # ПЕРЕНАПРАВЛЕНИЕ ПОСЛЕ УСПЕШНОГО СОХРАНЕНИЯ
            # redirect() перенаправляет пользователя на другую страницу
            # 'success_url' - имя URL-маршрута в urls.py
            return redirect('success_url')
    
    # ОБРАБОТКА GET-ЗАПРОСА (первое открытие страницы)
    else:
        """
        Когда пользователь просто заходит на страницу формы,
        браузер отправляет GET-запрос без данных
        """
        
        # СОЗДАЕМ ПУСТУЮ ФОРМУ ДЛЯ ЗАПОЛНЕНИЯ
        form = MyForm()
    
    # РЕНДЕРИНГ ШАБЛОНА С ФОРМОЙ
    # Выполняется в двух случаях:
    # 1. При GET-запросе (показ пустой формы)
    # 2. При POST-запросе с ошибками (показ формы с ошибками)
    return render(request, 'form.html', {'form': form})

3.1 Разбор формы:

from django import forms
from .models import MyModel  # Импортируем модель

class MyForm(forms.ModelForm):
    """
    ФОРМА НА ОСНОВЕ МОДЕЛИ (ModelForm)
    Автоматически создает поля на основе модели
    """
    class Meta:
        model = MyModel  # Связываем форму с моделью
        fields = ['name', 'email', 'message']  # Поля для отображения
        
        # Дополнительные настройки полей
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        
        # Подписи полей
        labels = {
            'name': 'Ваше имя',
            'email': 'Email адрес',
            'message': 'Сообщение'
        }

4. поиск и фильтрация:

from django.shortcuts import render
from django.db.models import Q  # Импортируем Q для сложных запросов
from .models import Product  # Импортируем модель товаров

def search_view(request):
    """
    ФУНКЦИЯ ПОИСКА - обработка поисковых запросов по товарам
    
    Обрабатывает GET-параметры для поиска по названию и описанию товаров
    """
    
    # ПОЛУЧЕНИЕ ПОИСКОВОГО ЗАПРОСА ИЗ URL
    # request.GET - словарь с параметрами из URL (после ?)
    # .get('q', '') - получаем значение параметра 'q' или пустую строку по умолчанию
    # Пример: /search/?q=iphone → query = 'iphone'
    # Пример: /search/ → query = '' (пустая строка)
    query = request.GET.get('q', '')
    
    # ИНИЦИАЛИЗАЦИЯ ПУСТОГО СПИСКА РЕЗУЛЬТАТОВ
    results = []  # Будет содержать найденные товары
    
    # ПРОВЕРКА: ЕСТЬ ЛИ ПОИСКОВЫЙ ЗАПРОС
    if query:
        """
        Поиск выполняется только если query не пустая строка
        """
        
        # ВЫПОЛНЕНИЕ ПОИСКОВОГО ЗАПРОСА К БАЗЕ ДАННЫХ
        # Q-объекты позволяют строить сложные запросы с OR, AND условиями
        results = Product.objects.filter(
            # Q-объект с оператором | (OR) - поиск по имени ИЛИ описанию
            Q(name__icontains=query) | Q(description__icontains=query)
            # __icontains - поиск подстроки без учета регистра
            # name__icontains='iphone' найдет: 'iPhone', 'iphone', 'IPHONE case'
        )
    
    # ПОДГОТОВКА ДАННЫХ ДЛЯ ШАБЛОНА
    context = {
        'results': results,  # Список найденных товаров
        'query': query,      # Поисковый запрос для отображения в форме
        'results_count': len(results)  # Количество найденных результатов
    }
    
    # РЕНДЕРИНГ ШАБЛОНА ПОИСКА
    return render(request, 'search.html', context)

5 Декоратор:

from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed

# ДЕКОРАТОР @login_required
@login_required  # Требует авторизации пользователя
def private_page(request):
    """
    СТРАНИЦА ТОЛЬКО ДЛЯ АВТОРИЗОВАННЫХ ПОЛЬЗОВАТЕЛЕЙ
    
    Декоратор @login_required автоматически:
    - Проверяет, авторизован ли пользователь
    - Если НЕТ - перенаправляет на страницу входа (settings.LOGIN_URL)
    - Если ДА - выполняет функцию
    """
    # request.user доступен и содержит объект пользователя
    user = request.user  # Авторизованный пользователь
    
    context = {
        'user': user,
        'message': f'Добро пожаловать, {user.username}!'
    }
    return render(request, 'private.html', context)


# ДЕКОРАТОР @permission_required
@permission_required('app.add_product', login_url='/custom-login/')  # Требует конкретного права
def add_product(request):
    """
    СТРАНИЦА ТОЛЬКО ДЛЯ ПОЛЬЗОВАТЕЛЕЙ С КОНКРЕТНЫМ ПРАВОМ
    
    Декоратор @permission_required проверяет:
    - Авторизован ли пользователь (@login_required включен автоматически)
    - Есть ли у пользователя указанное право
    
    Параметры:
    'app.add_product' - разрешение в формате 'приложение.код_права'
    login_url - необязательный параметр, куда перенаправлять при отказе
    """
    
    if request.method == 'POST':
        # Логика добавления товара
        # Только пользователи с правом 'app.add_product' смогут выполнить POST
        return redirect('product_list')
    
    # GET-запрос - показ формы добавления
    return render(request, 'add_product.html')


# ДЕКОРАТОР @require_http_methods
@require_http_methods(["GET", "POST"])  # Разрешает только указанные HTTP-методы
def contact_form(request):
    """
    ФОРМА КОНТАКТОВ, КОТОРАЯ РАБОТАЕТ ТОЛЬКО С GET И POST
    
    Декоратор @require_http_methods ограничивает допустимые HTTP-методы:
    - Если запрос GET или POST - функция выполняется
    - Если запрос PUT, DELETE и т.д. - возвращается HttpResponseNotAllowed (405)
    """
    
    if request.method == 'POST':
        # Обработка отправки формы
        name = request.POST.get('name')
        email = request.POST.get('email')
        # ... обработка данных
        return redirect('thank_you')
    
    # GET-запрос - показ формы
    return render(request, 'contact_form.html')


# КОМБИНАЦИЯ ДЕКОРАТОРОВ
@login_required
@permission_required('app.view_reports', raise_exception=True)
@require_http_methods(["GET"])
def reports_page(request):
    """
    КОМБИНАЦИЯ НЕСКОЛЬКИХ ДЕКОРАТОРОВ
    
    Порядок важен! Декораторы выполняются снизу вверх:
    1. @require_http_methods - проверяет метод запроса
    2. @permission_required - проверяет права
    3. @login_required - проверяет авторизацию
    
    Параметр raise_exception=True - вместо перенаправления вызывает исключение 403
    """
    reports = Report.objects.filter(user=request.user)
    return render(request, 'reports.html', {'reports': reports})

6. Пагинатор:

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import Article  # ваша модель

from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Note

def notes_list(request):
    # 1. Получаем ВСЕ данные
    all_notes = Note.objects.all().order_by('-created_at')
    
    # 2. Создаем пагинатор: (что пагинируем, сколько на страницу)
    paginator = Paginator(all_notes, 4)  # 4 заметки на страницу
    
    # 3. Получаем номер текущей страницы из URL
    page_number = request.GET.get('page')  # из ?page=2
    
    # 4. Получаем объект текущей страницы
    page_obj = paginator.get_page(page_number)
    
    # 5. Передаем в шаблон только объект страницы
    return render(request, 'notes/list.html', {
        'page_obj': page_obj  # ← ключевой момент!
    })
'''