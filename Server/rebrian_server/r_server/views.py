from rest_framework import generics

from .serializer import ClientSerializer
from .models import Client


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
