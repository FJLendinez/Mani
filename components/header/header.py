from django_components import component


@component.register("header")
class HeaderComponent(component.Component):
    template_name = 'header/header.html'


@component.register("sidebar")
class SidebarComponent(component.Component):
    template_name = 'header/sidebar.html'
