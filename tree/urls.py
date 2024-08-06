from django.urls import path, re_path
from .views import test_menu


urlpatterns = [
    re_path(r'^(?P<path>.*)/$', test_menu, name='test_menu'),
]
