from django.contrib import admin
from .models import Book, Category


# Setting Admin view of Book model's records
# in Django admin platform
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'category',
        'format',
        'book_depository_stars',
        'price',
        'isbn',
    )

    ordering = ('category',)


# Setting Admin view of Category model's records
# in Django admin platform
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


# Registering Book and Category models
# on Django admin platform
admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)
