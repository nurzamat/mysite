from django.contrib import admin
from azat.models import Post, Image, Category, Order
from mptt.admin import MPTTModelAdmin


# Register your models here.
class ImageInline(admin.TabularInline):
    model = Image


class PostAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]


#admin.site.register(UserProfile)
admin.site.register(Order)
admin.site.register(Image)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, MPTTModelAdmin)
