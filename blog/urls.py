from django.conf.urls import url

from .views import OwnPosts, Feed, Bloggers, Subscribe, Unsubscribe, Hide, PostDetail

urlpatterns = [
    url(r'^$', OwnPosts.as_view(), name='my_posts'),
    url(r'^feed/$', Feed.as_view(), name='feed'),
    url(r'^bloggers/$', Bloggers.as_view(), name='bloggers'),
    url(r'^(?P<user>[-\w]+)/(?P<pk>[-\w]+)/$', PostDetail.as_view(), name='post_detail'),
    url(r'^subscribe/$', Subscribe.as_view(), name='subscribe'),
    url(r'^unsubscribe/$', Unsubscribe.as_view(), name='unsubscribe'),
    url(r'^hide/$', Hide.as_view(), name='hide'),
]
