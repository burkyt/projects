from django.contrib import admin
from django.utils.html import format_html

from conf.models import Event, Category, Author, Product, Cart, Task


class EventAdmin(admin.ModelAdmin):
    filter_horizontal = ('author',)

    def image_tag(self, obj):
        return format_html('<img src="{} " style="max-width:200px; max-height:200px"/>'.format(obj.image.url))

    image_tag.short_description = 'Background'
    list_display = ['title', 'image_tag', ]


admin.site.register(Category)
admin.site.register(Event, EventAdmin)
admin.site.register(Author)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Task)
