from django.contrib import admin

from .models import Author, AuthorDetail, Category, Library, Member


admin.site.register(Author)
admin.site.register(AuthorDetail)
admin.site.register(Category)
admin.site.register(Member)


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}

