from django.urls import path, include

from .views import *

urlpatterns = [
    path('', index_page, name='home'),
    path('client/<int:client_id>/', get_client, name='get_client'),
    path('api/clients/', ClientViewSet.as_view()),
    path('api/clients/<int:pk>', ClientDetailView.as_view()),
    path('api/clients/add', ClientAddView.as_view()),
    # path('clients/<slug:name_slug>', ClientViewSet.as_view(), name='name'),
]
