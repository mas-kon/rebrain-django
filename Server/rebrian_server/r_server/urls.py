from django.urls import path, include

from .views import *

urlpatterns = [
    path('clients/', ClientViewSet.as_view()),
    path('clients/<int:pk>', ClientDetailView.as_view()),
    path('clients/add', ClientAddView.as_view()),
    # path('clients/<slug:name_slug>', ClientViewSet.as_view(), name='name'),
]
