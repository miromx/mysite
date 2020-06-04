from django.shortcuts import render, get_object_or_404, redirect
from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from mysite.urls import path
from django.core.mail import send_mail


# вьюха это контроллер!!

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('login')


def contact(request):
    '''
    тестовая херня
    :param request:
    :return:
    '''
    # objects = ['john', 'paul', 'ringo', 'star', 'john1', 'paul-1', 'ringo-1', ]
    #
    # paginator = Paginator(objects, 2)
    # page_num = request.GET.get('page', 1)
    # page_objects = paginator.get_page(page_num)
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'kleonorm@ya.ru',
                             ['kleonorm@gmail.com'], fail_silently=False)
            if mail:
                messages.success(request, 'Письмо отправлено!')
                return redirect('contact')
            else:
                messages.error(request, 'Ошибка отправки!')
        else:
            messages.error(request, 'Ошибка валидации!')
    else:
        form = ContactForm()
    return render(request, 'news/test.html', {'form': form})


class HomeNews(ListView, MyMixin):
    """
    если используются спсичные данные
    """
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    extra_context = {
        'title': 'Главная',
    }  # только для статичных днных

    mixin_prop = 'Hello world'
    paginate_by = 2  # по сколько новостей из списка выводить

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        """
        чтобы показывать только опубликованные данные
        :return: только опубликованные данные
        """
        return News.objects.filter(is_published=True).select_related('category')


# Create your views here.

# def index(request):
#     news = News.objects.order_by('-created_at')
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#         'fuck': 'хуйня, ебать...'
#     }
#     return render(request, template_name='news/index.html', context=context)


def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)

    return render(request, 'news/category.html', {'news': news, 'category': category})


class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False  # не показывать пустые списки
    paginate_by = 2  # по сколько новостей из списка выводить

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {'news_item': news_item})


class ViewNews(DetailView):
    model = News
    # template_name = 'news/news_detail.html'
    # pk_url_kwarg = 'news_id' # чтобы адрес менялся в конце числом
    context_object_name = 'news_item'


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)  # заполнили форму
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # news = News.objects.create(**form.cleaned_data) #распаковка словар, только для кастомных форм
#             news = form.save()
#             # return redirect('home') #на главную
#             return redirect(news)  # на созданную новсть
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})

class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # login_url = '/admin/'
    raise_exception = True
    # success_url = reverse_lazy('home') #редирект на главную
