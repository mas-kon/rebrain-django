from django import template
from r_server.models import Client

register = template.Library()


@register.simple_tag(name='get_all_clients')
def get_client():
    return Client.objects.all()


@register.inclusion_tag('news/list_categories.html')
def show_clients(arg1='Hello', arg2='world'):
    categories = Client.objects.all()
    return {"categories": categories, "arg1": arg1, "arg2": arg2}
