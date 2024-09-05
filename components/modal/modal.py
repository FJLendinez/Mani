from django_components import component


@component.register("modal")
class ModalComponent(component.Component):
    template_name = 'modal/modal.html'
