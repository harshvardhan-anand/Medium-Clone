# creating custom filter for django admin
# https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#:~:text=django.contrib.admin.SimpleListFilter
# https://timonweb.com/django/adding-custom-filters-to-django-admin-is-easy/

# https://pypi.org/project/django-admin-numeric-filter/

from django.contrib import admin
from admin_numeric_filter.admin import NumericFilterModelAdmin, RangeNumericFilter
from .models import Clap, Comment, Post, Tag
from user_info.models import Person

# Register your models here.

admin.site.register(Tag)

# NumericFilterModelAdmin itself inherits from admin.ModelAdmin so we don't need to inherit from admin.ModelAdmin
@admin.register(Post)
class PostAdmin(NumericFilterModelAdmin):
    list_display = ('author', 'title', 'created', 'total_claps', 'status')
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('author',)
    search_fields = ('title', 'body', 'author__username')
    list_editable = ('status',)
    list_per_page = 20
    list_filter = (
        'created',
        ('total_claps', RangeNumericFilter), 
    )

@admin.register(Clap)
class ClapAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'claps_given', 'created')
    search_field = ('user', 'post')
    list_filter =  ('claps_given', 'created')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'comment', 'created')
    search_fields = ('user', 'post', 'comment')
    list_filter =  ('created',)