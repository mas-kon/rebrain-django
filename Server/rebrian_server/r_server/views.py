from rest_framework import generics
from django.shortcuts import render, get_object_or_404
from .serializer import ClientSerializer
from .models import Client


def index_page(request):
    context = {
        'title': 'Клиенты'}
    return render(request, template_name='r_server/index.html', context=context)


def get_client(request, client_id):
    # client_item = Client.objects.get(pk=client_id)
    client_item = get_object_or_404(Client, pk=client_id)
    return render(request, 'r_server/client.html', {'client_item': client_item})


class ClientAddView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientViewSet(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ExceptionLoggingMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # print(request.body)
        # print(request.scheme)
        # print(request.method)
        # print(request.META)

        response = self.get_response(request)

        return response
