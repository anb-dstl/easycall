from django.urls import path
from django.urls import re_path
from ezcall import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index),
    path('create', views.create),
    path('delete', views.delete),
    path('calling', views.calling),
    #path('delete/<int:id>/', views.delete),
    re_path(r'^', views.index),
]
urlpatterns += [
    re_path(r'^robots\.txt$', TemplateView.as_view(template_name="ezcall/robots.txt", content_type='text/plain')),
]