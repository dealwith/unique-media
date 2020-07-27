from django.urls import path
from . import views


urlpatterns = [
    path('', views.list),
    path('list', views.list, name='cloud_functional.views.list'),
    path('upload', views.upload, name='cloud_functional.views.upload'),
    path('upload/complete', views.direct_upload_complete, name='cloud_functional.views.direct_upload_complete'),
]
