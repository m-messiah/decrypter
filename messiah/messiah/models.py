# ~*~ coding: utf-8 ~*~

# импортируем класс модели
from django.db import models
# и админки
from django.contrib import admin

'''
Blog posts
'''


class Post(models.Model):
    # название поста
    title = models.CharField(max_length=100)
    # содержимое поста
    text = models.TextField()

    # функция необходима для того, чтобы при выводе объекта Post
    # как строки выводился вместо этого его title
    def __unicode__(self):
        return self.title


'''
Класс для админки, тут будут дополнительные атрибуты необходимые для админки
'''


class PostAdmin(admin.ModelAdmin):
    # в таблице списка постов выводить только колонку title,
    # если вы добавите еще одно имя поля, то и оно выведется
    list_display = ('title',)

# связываем эту модель с моделью PostAdmin
admin.site.register(Post, PostAdmin)
