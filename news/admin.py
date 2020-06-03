from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe
from django import forms

from .models import News, Category  # для отображения на админской панели
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):  # кастомизация News
    form = NewsAdminForm
    list_display = ['id', 'title', 'category', 'created_at', 'updated_at', 'is_published', 'get_photo']
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category',)

    fields = ('title', 'category', 'content', 'photo', 'get_photo', 'is_published', 'views',
              'created_at', 'updated_at',)

    readonly_fields = ('get_photo', 'views', 'created_at', 'updated_at',)

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')
        else:
            return 'Нет фото'

    get_photo.short_description = 'Миниатюра'
    save_on_top = True


class CategoryAdmin(admin.ModelAdmin):  # кастомизация News
    list_display = ['id', 'title']
    list_display_links = ('id', 'title')
    search_fields = ('title',)


admin.site.register(News, NewsAdmin)  # порядоок важен!!
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Управление сайтом'
admin.site.site_header = 'Управление сайтом'
