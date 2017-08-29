from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('blog.urls')),
    url(r'^logout', auth_views.logout, {'template_name': 'app/login.html', 'next_page': 'login'}, name='logout'),
    url(r'^login', auth_views.login, {'template_name': 'app/login.html'}, name='login')
]
