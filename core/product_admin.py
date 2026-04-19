from django.contrib import admin


class BaseProductAdmin(admin.ModelAdmin):
    list_per_page = 25
    readonly_fields = ('image_tag',)
    search_fields = ('name', "id")


class RichProductAdmin(BaseProductAdmin):
    list_display = ('id', 'name', 'price', 'image_tag', 'details', 'description')


class FeaturedProductAdmin(BaseProductAdmin):
    list_display = ('id', 'name', 'price', 'image_tag')
