from django.db import models
from django.urls import reverse_lazy


# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    content = models.TextField(blank=True, verbose_name='Контент')  # необязатллллльено к заполнению
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')  # дата созадния не меняется
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    # связь с категориями
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True,
                                 verbose_name='Категория')  # защита от удаления связанных новостей
    views = models.IntegerField(default=0)

    def my_func(self):
        return 'Hello from model'

    def get_absolute_url(self):
        return reverse_lazy('view_news', kwargs={"pk": self.pk})

    def __str__(self):
        return self.title  # представление в нормальном читаемом виде

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at', 'title']


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Наименование категории')

    def get_absolute_url(self):
        return reverse_lazy('category', kwargs={"category_id": self.pk})

    def __str__(self):
        return self.title  # представление в нормальном читаемом виде

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']
