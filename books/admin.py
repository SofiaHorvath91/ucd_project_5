from django.contrib import admin
from .models import Book, Category


# Register your models here.
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


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)

