from django.contrib import admin

from blog.models import Blogger, Hidden, Post


admin.site.register(Blogger)
admin.site.register(Hidden)
admin.site.register(Post)
