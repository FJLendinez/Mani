from django_components import component


@component.register("messages")
class MessagesComponent(component.Component):
    template_name = 'messages/messages.html'
